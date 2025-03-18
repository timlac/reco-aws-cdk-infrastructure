# Road map 

## Get Surveys from API

The maximum payload size of API Gateway is 10MB. This puts a limit on the number of surveys at around 250 surveys. 

Improvements would need to involve:

- Get Surveys endpoint that does not return survey items. 
- Custom endpoints for statistics on survey items:
  - emotions in all surveys and finished surveys 
  - time spent on each survey. 
  - average time spent on each item (optional)
- The frontend would need to invoke get survey when the user clicks on a survey to get to survey details.
- API endpoint with lambda that organizes (in user-friendly format) and compresses all surveys and 
returns the compressed object to the frontend for export.



