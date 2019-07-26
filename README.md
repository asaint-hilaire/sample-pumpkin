# sample-pumpkin
#### To create the development environment

Install dependencies

`npm i`

`pipenv sync -d`

`pipenv shell`

Install dynamodb

`sls dynamodb install`

Run serverless local dynamodb

`sls dynamodb start`

Run serverless local wsgi

`sls wsgi serve`

#### Generate metrics

`npm run codeMetrics`

#### Endpoints

`POST pets/{petId}/quote` this endpoint generates a quote for the pet requested. I decided to implement it as a post because it is doing a calculation and comforms to the description of a rest controller archetype. 

`GET pets` returns a collection of pets

`GET pets/{petId}` returns a specific pet

`POST pets` creates a pet

I only implemented these four methods since the endpoints are public and no user is associated with any pet I didn't think it was correct to give anyone access to update or delete any pets.
