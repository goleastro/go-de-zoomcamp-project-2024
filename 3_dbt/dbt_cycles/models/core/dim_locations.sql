select
    Site_ID,
    Location_description as Location,
    Borough,
    Functional_area_for_monitoring as Functional_area,
    Road_type--,
    --Is_it_on_the_strategic_CIO_panel as CIO_panel,
    --Old_site_ID_legacy,
    --Easting_UK_Grid,
    --Northing_UK_Grid,
    --Latitude,
    --Longitude
from {{ ref('monitoring_locations_lookup') }}