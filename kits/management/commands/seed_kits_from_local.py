import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from kits.models import Kit

AUDIO_EXTS = {".wav", ".aif", ".aiff", ".mp3", ".flac", ".ogg"}


def unique_slug(base_slug: str) -> str:
    if not Kit.objects.filter(slug=base_slug).exists():
        return base_slug

    i = 2
    while True:
        candidate = f"{base_slug}-{i}"
        if not Kit.objects.filter(slug=candidate).exists():
            return candidate
        i += 1


class Command(BaseCommand):
    help = "Seed kits from a local samples folder: one kit per folder, samples[] = relative file paths."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Do not write to DB.")
        parser.add_argument(
            "--samples-dir",
            type=str,
            default="samples",
            help="Local folder that contains kit folders (default: ./samples).",
        )

    def handle(self, *args, **opts):
        dry_run = opts["dry_run"]
        samples_dir = Path(opts["samples_dir"]).resolve()

        if not samples_dir.exists() or not samples_dir.is_dir():
            self.stdout.write(self.style.ERROR(f"Samples directory not found: {samples_dir}"))
            return

        kit_folders = sorted([p for p in samples_dir.iterdir() if p.is_dir()])
        self.stdout.write(f"Found {len(kit_folders)} kit folders under '{samples_dir}'")

        created = 0
        updated = 0

        # Store paths relative to project root (so they’re portable)
        project_root = Path.cwd().resolve()

        for folder_path in kit_folders:
            kit_name = folder_path.name
            base_slug = slugify(kit_name)

            # Collect audio files (non-recursive)
            sample_paths = []
            for file_path in sorted(folder_path.iterdir()):
                if not file_path.is_file():
                    continue

                ext = file_path.suffix.lower()
                if ext not in AUDIO_EXTS:
                    continue

                rel = file_path.resolve().relative_to(project_root)
                # e.g. "samples/Roland TR808/kick.wav"
                sample_paths.append(str(rel))

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
                if kit.samples != sample_paths:
                    kit.samples = sample_paths
                    kit.save(update_fields=["samples", "updated_at"])
                    updated += 1

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry run complete. No DB writes."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}, Updated: {updated}"))