# Charik Backend Developer Technical Test

## Introduction

Welcome to the Charik Backend Developer Technical Test. This repository contains the solution for the test, which is designed to assess your technical skills in Django REST Framework, Docker, and HubSpot integration. The project includes endpoints to create contacts and deals in HubSpot, associate them, and retrieve the information.



# Getting Started

## Clone the Repository

To get started, clone the repository:

```bash
git clone https://github.com/Ghobrini/Charik-Backend-Interview---Ghobrini.git
cd Charik-Backend-Interview---Ghobrini
```
## Setup Environment

### Install Dependencies
Ensure Docker and Docker Compose are installed on your machine.

### Configure Environment Variables
add the following variables in your credentials.env
```
HUBSPOT_API_KEY=[Your HubSpot API will be in the email]
```
#### scope
  - `crm.objects.deals.read`
  - `crm.objects.deals.write`
  - `crm.objects.contacts.read`
  - `crm.objects.contacts.write`

### Build and Start Docker Containers
```
docker-compose up 
```
The application will be available at http://localhost:8083.

## API Documentation

### Contact:

#### Contact Creation :

- **Endpoint :**`/core/contact/`
- **Method :**`POST`
- **Description :**`Create a contact`
- **Request Body :**

```json
   {
    "email": "ghob@gmail.com",
    "firstname": "Abdelkader",
    "lastname": "Ghobrini",
    "company": "HubSpot",
    "website": "hubspot.com"
    }
```
- **Response :**

```json
   {
    "created_at": "2024-08-26T14:31:18.439000Z",
    "archived": false,
    "archived_at": null,
    "properties_with_history": null,
    "id": "32059711937",
    "properties": {
        "company": "HubSpot",
        "createdate": "2024-08-26T14:31:18.439Z",
        "email": "ghob3@gmail.com",
        "firstname": "test3_Abdelkader",
        "hs_all_contact_vids": "32059711937",
        "hs_email_domain": "gmail.com",
        "hs_is_contact": "true",
        "hs_is_unworked": "true",
        "hs_lifecyclestage_lead_date": "2024-08-26T14:31:18.439Z",
        "hs_marketable_status": "false",
        "hs_marketable_until_renewal": "false",
        "hs_membership_has_accessed_private_content": "0",
        "hs_object_id": "32059711937",
        "hs_object_source": "INTEGRATION",
        "hs_object_source_id": "3772530",
        "hs_object_source_label": "INTEGRATION",
        "hs_pipeline": "contacts-lifecycle-pipeline",
        "hs_registered_member": "0",
        "lastmodifieddate": "2024-08-26T14:31:18.439Z",
        "lastname": "test3_Ghobrini",
        "lifecyclestage": "lead",
        "website": "http://hubspot.com"
    },
    "updated_at": "2024-08-26T14:31:18.439000Z"
}
```

### Deal:

#### Deal Creation :

- **Endpoint :**`/core/deal/`
- **Method :**`POST`
- **Description :**`Create a deal`
- **Request Body :**

```json
   {
    "amount": "150.00",
    "closedate": "2024-12-07T16:50:06.678Z",
    "dealname": "New depxal"
   }
```
- **Response :**

```json
{
    "created_at": "2024-08-26T14:37:49.792000Z",
    "archived": false,
    "archived_at": null,
    "properties_with_history": null,
    "id": "16464914367",
    "properties": {
        "amount": "150.00",
        "amount_in_home_currency": "150.00",
        "closedate": "2024-12-07T16:50:06.678Z",
        "createdate": "2024-08-26T14:37:49.792Z",
        "days_to_close": "103",
        "dealname": "New depxal",
        "hs_closed_amount": "0",
        "hs_closed_amount_in_home_currency": "0",
        "hs_closed_won_count": "0",
        "hs_createdate": "2024-08-26T14:37:49.792Z",
        "hs_days_to_close_raw": "103.091862",
        "hs_deal_stage_probability_shadow": "0",
        "hs_forecast_amount": "150.00",
        "hs_is_closed_lost": "false",
        "hs_is_closed_won": "false",
        "hs_is_deal_split": "false",
        "hs_lastmodifieddate": "2024-08-26T14:37:49.792Z",
        "hs_object_id": "16464914367",
        "hs_object_source": "INTEGRATION",
        "hs_object_source_id": "3772530",
        "hs_object_source_label": "INTEGRATION",
        "hs_projected_amount": "0",
        "hs_projected_amount_in_home_currency": "0"
    },
    "updated_at": "2024-08-26T14:37:49.792000Z"
}
```

### Associate:

#### Association Creation :

- **Endpoint :**`/core/associate/`
- **Method :**`POST`
- **Description :**`Create an association between contact & deal`
- **Request Body :**

```json
   {"deal_id": "16464914367","contact_id": "32059711937"}
```
- **Response :**`STATUS 200`

```json
   {
    "completed_at": "2024-08-26T17:22:12.370000Z",
    "requested_at": null,
    "started_at": "2024-08-26T17:22:12.308000Z",
    "links": null,
    "results": [
        {
            "_from": {
                "id": "16464914367"
            },
            "to": {
                "id": "32059711937"
            },
            "type": "deal_to_contact"
        },
        {
            "_from": {
                "id": "32059711937"
            },
            "to": {
                "id": "16464914367"
            },
            "type": "contact_to_deal"
        }
    ],
    "status": "COMPLETE"
}
```

#### Fetch Associate  :

- **Endpoint :**`/core/associate/`
- **Method :**`GET`
- **Description :**`Create an association between contact & deal`


#### Fetch Associates:

- **Endpoint:** `/core/associate/`
- **Method:** `GET`
- **Description:** `Retrieve a list of contacts and their associated deals with support for pagination.`
- **Query Parameters:**
  - `after` (optional): The starting point for fetching the next page of results. If not provided, the results will start from the beginning.
  - `limit` (optional): The number of contacts to retrieve per page. Defaults to 50 if not provided.
- **Response:**
  If pagination is applied:

```json
{
    "next": {
        "link": "http://0.0.0.0:8083/core/associate/?limit=25&after=32109216467",
        "after": "32109216467"
    },
    "results": [
        {
            "associations": null,
            "created_at": "2024-08-25T08:46:21.428000Z",
            "archived": false,
            "archived_at": null,
            "properties_with_history": null,
            "id": "31856923120",
            "properties": {
                "createdate": "2024-08-25T08:46:21.428Z",
                "email": "bh@hubspot.com",
                "firstname": "Brian",
                "hs_object_id": "31856923120",
                "lastmodifieddate": "2024-08-25T08:46:37.666Z",
                "lastname": "Halligan (Sample Contact)"
            },
            "updated_at": "2024-08-25T08:46:37.666000Z",
            "deals": []
        }]
}
```

if pagination is not applied 
```json
 [
        {
            "associations": null,
            "created_at": "2024-08-25T08:46:21.428000Z",
            "archived": false,
            "archived_at": null,
            "properties_with_history": null,
            "id": "31856923120",
            "properties": {
                "createdate": "2024-08-25T08:46:21.428Z",
                "email": "bh@hubspot.com",
                "firstname": "Brian",
                "hs_object_id": "31856923120",
                "lastmodifieddate": "2024-08-25T08:46:37.666Z",
                "lastname": "Halligan (Sample Contact)"
            },
            "updated_at": "2024-08-25T08:46:37.666000Z",
            "deals": []
        }]
```