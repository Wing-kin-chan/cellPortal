# cellPortal
A lightweight web application for storing, visualizing, and exploring single-cell, and
spatial transcriptomics data that you want to publish. Built using Python, HTML5, and CSS, cellPortal
will leverage AWS (via boto3) Lambda, DynamoDB, and S3 to host data that peers may want
to reference.

### Technologies
- `AWS Lambda`
- `AWS DynamoDB`
- `AWS S3 Storage`
- Python `Flask`, `Dash`, & `Plotly`
- `HTML` & `CSS`

### Structure
- cellPortal Homepage with Explore, Publish, and About tabs:
    1. Explore tab has search bar and a few featured datasets.
    2. Publish tab contains information regarding publish, and login form.
    If and when logged in, redirects to account page to view user experiments,
    and upload data.
    3. About thab contains information regarding the website.
- Clicking on any experiment will redirect to a visualization page to display interactive plots.