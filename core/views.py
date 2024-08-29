import os

import hubspot
from hubspot.crm.deals import (
                        SimplePublicObjectInputForCreate as DealObjectCreate,
                        ApiException as DealException,
                        BatchReadInputSimplePublicObjectId as DealBatchObject)
from hubspot.crm.contacts import SimplePublicObjectInputForCreate as ContactObjectCreate, ApiException as ContactException 
from hubspot.crm.associations import BatchInputPublicAssociation, ApiException, BatchInputPublicObjectId

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.serializers import ContactSerialiser, DealSerialiser, AssociateSerialiser


# Initialize HubSpot client with access token
client = hubspot.Client.create(access_token=os.environ.get('HUBSPOT_ACCESS_TOKEN'))



class ContactView(APIView):
    """
    ContactView handles the creation of contact objects via POST requests.
    """

    def post(self, request, format=None):
        """
        Handle POST request to create a new contact.

        1. Deserialize the incoming request data using ContactSerialiser.
        2. If the data is valid, create a ContactObjectCreate instance with the validated data.
        3. Attempt to create the contact using HubSpot's API.
        4. Return the API response as JSON with HTTP status 200 if successful.
        5. If a contact already exists, catch the exception and return an appropriate error message with HTTP status 400.
        6. If the data is invalid, return the validation errors with HTTP status 400.
        """

        # Deserialize the request data using the ContactSerialiser
        serializer = ContactSerialiser(data=request.data)
        
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Create a ContactObjectCreate instance with the validated data
            contact_object = ContactObjectCreate(properties=serializer.data)
            
            try:
                # Attempt to create the contact using HubSpot's API
                api_response = client.crm.contacts.basic_api.create(
                    simple_public_object_input_for_create=contact_object
                )
                
                # If successful, return the API response as a JSON object with HTTP status 200
                return Response(api_response.to_dict(), status=status.HTTP_200_OK)
            
            except ContactException as e:
                # If the contact already exists, return a specific error message
                return Response(e.__dict__['body'], status=status.HTTP_400_BAD_REQUEST)
        
        # If the data is invalid, return the validation errors with HTTP status 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DealView(APIView):
    """
    DealView handles the creation of deal objects via POST requests.
    """

    def post(self, request, format=None):
        """
        Handle POST request to create a new deal.

        1. Deserialize the incoming request data using DealSerialiser.
        2. If the data is valid, create a DealObjectCreate instance with the validated data.
        3. Attempt to create the deal using HubSpot's API.
        4. Return the API response as JSON with HTTP status 200 if successful.
        5. If an exception occurs, return a generic error message with HTTP status 400.
        6. If the data is invalid, return the validation errors with HTTP status 400.
        """

        # Deserialize the request data using the DealSerialiser
        serializer = DealSerialiser(data=request.data)
        
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Create a DealObjectCreate instance with the validated data
            deal_object = DealObjectCreate(properties=serializer.data)
            
            try:
                # Attempt to create the deal using HubSpot's API
                api_response = client.crm.deals.basic_api.create(
                    simple_public_object_input_for_create=deal_object
                )
                
                # If successful, return the API response as a JSON object with HTTP status 200
                return Response(api_response.to_dict(), status=status.HTTP_200_OK)
            
            except DealException as e:
                # If an exception occurs during the API call, return a generic error message
                return Response(e.__dict__['body'], status=status.HTTP_400_BAD_REQUEST)
        
        # If the data is invalid, return the validation errors with HTTP status 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AssociateView(APIView):
    """
    AssociateView handles GET and POST requests related to associations between contacts and deals.
    """

    def get(self, request, format=None):
        """
        Handle GET request to retrieve contacts and their associated deals, with support for pagination.

        1. Retrieve query parameters for pagination: `after` (for next page) and `limit` (number of items per page).
        2. Fetch contacts based on pagination parameters.
        3. Extract contact IDs and fetch associations with deals.
        4. Retrieve deal details and associate them with contacts.
        5. Return paginated response with associated deals.
        """

        # Retrieve query parameters for pagination
        after = request.query_params.get('after')
        limit = request.query_params.get('limit')

        # Determine the appropriate limit for pagination
        if not limit:
                limit = 50
        if after:
            api_response = client.crm.contacts.basic_api.get_page(
                limit=limit, after=after, archived=False
            )
        else:
            api_response = client.crm.contacts.basic_api.get_page(
                limit=limit, archived=False
            )

        # Convert the API response to dictionary
        api_response = api_response.to_dict()
        
        # Extract contacts from the response
        contacts = api_response["results"]

        # Extract pagination information
        paging = api_response.get("paging")

        # Create a list of contact IDs for batch fetching associations
        contact_ids = [{"id": contact["id"]} for contact in contacts]
        association_object = BatchInputPublicObjectId(inputs=contact_ids)

        # Fetch associations between contacts and deals
        api_response = client.crm.associations.batch_api.read(
            from_object_type="contact", to_object_type="deal",
            batch_input_public_object_id=association_object
        )
        associations = api_response.to_dict()["results"]

        # Extract deal IDs from associations
        deal_ids = []
        for association in associations:
            for deal in association["to"]:
                deal_ids.append(deal["id"])
        
        # Remove duplicate deal IDs
        deal_ids = list(set(deal_ids))

        # Fetch details of the deals
        deal_objects = DealBatchObject(inputs=deal_ids)
        try:
            api_response = client.crm.deals.batch_api.read(
                batch_read_input_simple_public_object_id=deal_objects, archived=False
            )
            deals = api_response.to_dict()["results"]
        except DealException as e:
            return Response(e.__dict__['body'], status=status.HTTP_400_BAD_REQUEST)

        # Associate deals with each contact
        for contact in contacts:
            contact["deals"] = []
            for association in associations:
                if contact["id"] == association["_from"]["id"]:
                    for item in association["to"]:
                        for deal in deals:
                            if deal["id"] == item["id"]:
                                contact["deals"].append(deal)

        # Prepare pagination data for response
        if paging:
            data = {
                "next": {
                    "link": f"{request.build_absolute_uri(request.path)}?limit={limit}&after={paging['next']['after']}",
                    "after": paging["next"]['after']
                },
                "results": contacts
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(contacts, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Handle POST request to create associations between a contact and a deal.

        1. Deserialize the request data using AssociateSerialiser.
        2. Create a BatchInputPublicAssociation instance with contact and deal IDs.
        3. Attempt to create the association using HubSpot's API.
        4. Return the API response with HTTP status 200 if successful.
        5. Handle exceptions and return an error message with HTTP status 400 if any issues occur.
        """

        # Deserialize the request data using AssociateSerialiser
        serializer = AssociateSerialiser(data=request.data)
        
        # Check if the serialized data is valid
        if serializer.is_valid():
            # Create a BatchInputPublicAssociation instance with contact and deal IDs
            batch_input_public_association = BatchInputPublicAssociation(
                inputs=[{
                    "from": {"id": request.data["contact_id"]},
                    "to": {"id": request.data["deal_id"]},
                    "type": "contact_to_deal"
                }]
            )

            try:
                # Attempt to create the association using HubSpot's API
                api_response = client.crm.associations.batch_api.create(
                    from_object_type="contact", to_object_type="deal",
                    batch_input_public_association=batch_input_public_association
                )
                # Return the API response with HTTP status 200 if successful
                return Response(api_response.to_dict(), status=status.HTTP_200_OK)
            
            except ApiException as e:
                # Return an error message with HTTP status 400 if an exception occurs
                return Response(e.__dict__['body'], status=status.HTTP_400_BAD_REQUEST)
        
        # Return validation errors with HTTP status 400 if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)