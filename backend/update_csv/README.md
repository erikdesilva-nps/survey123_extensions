# Update CSV
This script is used to update hosted comma separated value files (.csv) on ArcGIS Online or a portal instance. Hosted comma separated value files are typically used in [linked content](https://community.esri.com/t5/arcgis-survey123-blog/survey123-tricks-of-the-trade-configuring-survey-maps/ba-p/897815) <font style="font-family: monospace">select_one_from_file</font> or <font style="font-family: monospace">select_multiple_from_file</font> question types in Survey123.
## Prerequisites

* Credentials for a SQL server user with access to the target table saved in the [Windows Credential Manager](https://support.microsoft.com/en-us/windows/accessing-credential-manager-1b5c916a-6a16-889f-8581-fc16e8165ac0), saved as 'Generic Credentials'
* Credentials for the user which owns the target hosted .csv file saved in the [Windows Credential Manager](https://support.microsoft.com/en-us/windows/accessing-credential-manager-1b5c916a-6a16-889f-8581-fc16e8165ac0), saved as 'Generic Credentials'
* [Item ID](https://community.esri.com/t5/arcgis-online-blog/where-can-i-find-the-item-id-for-an-arcgis-online-item/ba-p/890284) for the target hosted .csv file

## Example Usage

<pre><code>from update_survey_lcontent import update_picklists
update_picklists(item_id='65a3fed8a716456cbb066a972ce9e075',
                 sql_schema='example_schema',
                 table_name='example_table',
                 field_map={'example_name': 'name',
                            'example_label': 'label'})</code></pre>