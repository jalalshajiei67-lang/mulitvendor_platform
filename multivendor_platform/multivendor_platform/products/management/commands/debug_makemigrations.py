# products/management/commands/debug_makemigrations.py
import json
import os
import time
import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO

LOG_PATH = "/media/jalal/New Volume/project/mulitvendor_platform/.cursor/debug.log"

def log_debug(session_id, run_id, hypothesis_id, location, message, data=None):
    """Log debug information to file"""
    try:
        log_entry = {
            "sessionId": session_id,
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(time.time() * 1000)
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Silently fail if logging doesn't work


class Command(BaseCommand):
    help = 'Debug makemigrations to understand migration issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            help='Run makemigrations --check',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run makemigrations --dry-run',
        )

    def handle(self, *args, **options):
        # #region agent log
        log_debug(
            "debug-session",
            "run1",
            "A",
            "debug_makemigrations.py:handle",
            "Command started",
            {"check": options.get("check", False), "dry_run": options.get("dry_run", False)}
        )
        # #endregion

        check = options.get('check', False)
        dry_run = options.get('dry_run', False)

        # #region agent log
        log_debug(
            "debug-session",
            "run1",
            "B",
            "debug_makemigrations.py:handle",
            "About to run makemigrations",
            {"check": check, "dry_run": dry_run}
        )
        # #endregion

        try:
            # Capture stdout/stderr
            stdout_capture = StringIO()
            stderr_capture = StringIO()

            # Build command arguments
            cmd_args = ['products']
            if check:
                cmd_args.append('--check')
            if dry_run:
                cmd_args.append('--dry-run')

            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "C",
                "debug_makemigrations.py:handle",
                "Calling makemigrations",
                {"cmd_args": cmd_args}
            )
            # #endregion

            # Run makemigrations
            call_command('makemigrations', *cmd_args, stdout=stdout_capture, stderr=stderr_capture)

            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()

            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "D",
                "debug_makemigrations.py:handle",
                "makemigrations completed successfully",
                {"stdout": stdout_output, "stderr": stderr_output}
            )
            # #endregion

            self.stdout.write(self.style.SUCCESS('makemigrations completed successfully'))
            if stdout_output:
                self.stdout.write(stdout_output)
            if stderr_output:
                self.stdout.write(self.style.WARNING(stderr_output))

        except SystemExit as e:
            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "E",
                "debug_makemigrations.py:handle",
                "makemigrations failed with SystemExit",
                {"exit_code": e.code}
            )
            # #endregion
            self.stdout.write(self.style.ERROR(f'makemigrations failed with exit code: {e.code}'))
            raise
        except Exception as e:
            # #region agent log
            log_debug(
                "debug-session",
                "run1",
                "F",
                "debug_makemigrations.py:handle",
                "makemigrations failed with exception",
                {"error_type": type(e).__name__, "error_message": str(e)}
            )
            # #endregion
            self.stdout.write(self.style.ERROR(f'makemigrations failed: {e}'))
            raise

