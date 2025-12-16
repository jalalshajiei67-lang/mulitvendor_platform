# Custom storage class to handle missing source map files
from whitenoise.storage import CompressedManifestStaticFilesStorage


class IgnoreMissingSourceMapsStorage(CompressedManifestStaticFilesStorage):
    """
    Custom storage class that ignores missing source map files (.map)
    when processing static files. This prevents collectstatic from failing
    when JavaScript files reference source maps that don't exist.
    
    Source maps are only needed for debugging and are not required for
    production, so it's safe to ignore missing source map files.
    """
    
    def stored_name(self, name):
        """
        Override to ignore missing source map files.
        """
        # If this is a source map file, try to process it but don't fail if missing
        if name.endswith('.map'):
            try:
                return super().stored_name(name)
            except ValueError:
                # Source map file doesn't exist - return original name
                # This allows collectstatic to continue without failing
                return name
        return super().stored_name(name)
    
    def _url(self, hashed_name_func, name, force=False, hashed_files=None):
        """
        Override to handle missing source map files gracefully.
        """
        if name.endswith('.map'):
            try:
                return super()._url(hashed_name_func, name, force, hashed_files)
            except ValueError:
                # Source map file doesn't exist - return original name
                return name
        return super()._url(hashed_name_func, name, force, hashed_files)
    
    def _post_process(self, paths, adjustable_paths, hashed_files):
        """
        Override post-processing to catch and ignore errors for missing source map files.
        """
        try:
            # Process files normally
            for name, hashed_name, processed_file, is_processed in super()._post_process(paths, adjustable_paths, hashed_files):
                yield name, hashed_name, processed_file, is_processed
        except ValueError as e:
            # Check if the error is about a missing source map file
            error_msg = str(e)
            if '.map' in error_msg and 'could not be found' in error_msg:
                # This is a missing source map file - we can safely ignore it
                # Source maps are only needed for debugging, not for production
                # Return empty generator to skip this file
                return
            # For other errors, re-raise them
            raise

