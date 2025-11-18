The Crowdin API has been extended with new Translation Import endpoints that provide a more efficient way to import translations. Additionally, the legacy translation upload method has been deprecated.

The Crowdin API client libraries need to be updated to include these new endpoints and mark the deprecated method accordingly.

New Endpoints:

Import Translations - Upload translation files for import
Check Translation Import Status - Get import operation status
Download Translation Import Report - Download detailed import report
Deprecated:

Upload Translations (Legacy) - This method is deprecated in favor of the new Import Translations endpoint
References:

Import Translations
Check Translation Import Status
Download Translation Import Report
Upload Translations (Legacy - Deprecated)