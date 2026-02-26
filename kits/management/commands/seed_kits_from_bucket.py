import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from supabase import create_client

from kits.models import Kit


AUDIO_EXTS = {".wav", ".aif", ".aiff", ".mp3", ".flac", ".ogg"}


def unique_slug(base_slug: str) -> str:
    """
    Ensure slug uniqueness by appending -2, -3, ...
    """
    if not Kit.objects.filter(slug=base_slug).exists():
        return base_slug

    i = 2
    while True:
        candidate = f"{base_slug}-{i}"
        if not Kit.objects.filter(slug=candidate).exists():
            return candidate
        i += 1


class Command(BaseCommand):
    help = "Seed Kit rows from Supabase Storage: one kit per folder, samples[] = storage paths."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Do not write to DB.")
        parser.add_argument(
            "--base-prefix",
            type=str,
            default=os.getenv("SUPABASE_BASE_PREFIX", "samples"),
            help="Storage prefix where kit folders live (default: env SUPABASE_BASE_PREFIX or 'samples').",
        )

    def handle(self, *args, **opts):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        bucket = os.getenv("SUPABASE_BUCKET", "drum-kits")
        base_prefix = (opts["base_prefix"] or "samples").strip("/")

        if not supabase_url or not supabase_key:
            self.stdout.write(self.style.ERROR("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env"))
            return

        sb = create_client(supabase_url, supabase_key)
        storage = sb.storage.from_(bucket)

        dry_run = opts["dry_run"]

        # List kit folders under base_prefix (e.g. "samples/")
        top_items = storage.list(base_prefix)
        kit_folders = sorted([obj.get("name") for obj in top_items if obj.get("name")])

        self.stdout.write(f"Found {len(kit_folders)} kit folders under '{base_prefix}/' in bucket '{bucket}'")

        created = 0
        updated = 0

        for folder_name in kit_folders:
            kit_name = folder_name
            base_slug = slugify(kit_name)

            # IMPORTANT: we keep exact folder name for paths
            folder_prefix = f"{base_prefix}/{folder_name}"

            items = storage.list(folder_prefix)

            sample_paths = []
            for it in items:
                filename = it.get("name")
                if not filename:
                    continue

                ext = Path(filename).suffix.lower()
                if ext not in AUDIO_EXTS:
                    continue

                # Store exact path as it exists in bucket
                sample_paths.append(f"{folder_prefix}/{filename}")

            # stable ordering (nice for diffs)
            sample_paths.sort()

            if dry_run:
                self.stdout.write(f"[DRY] {kit_name} | slug={base_slug} | samples={len(sample_paths)}")
                continue

            kit = Kit.objects.filter(name=kit_name).first()

            if kit is None:
                slug = unique_slug(base_slug)
                Kit.objects.create(
                    name=kit_name,
                    slug=slug,
                    description="",
                    image_path="",
                    samples=sample_paths,
                )
                created += 1
            else:
                # keep slug stable if it already exists
                changed = False
                if kit.samples != sample_paths:
                    kit.samples = sample_paths
                    changed = True

                # leave description/image_path empty for now, as requested
                if changed:
                    kit.save(update_fields=["samples", "updated_at"])
                    updated += 1

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry run complete. No DB writes."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))