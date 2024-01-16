'''Test the stability of the API'''
from rest_framework import status
from rest_framework.test import APITestCase


class DAWNetTests(APITestCase):
    '''API DAWNet Tests'''

    def setUp(self) -> None:
        '''Setup the client to contact the API'''
        self.headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'fr'
        }


    def test_dawnet(self) -> None:
        '''Test the dawnet API'''
        # GET /dawnet
        response = self.client.get('/api/dawnet',
            headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # GET /dawnet/id
        response = self.client.get(f'/api/dawnet/dawnet_id',
            headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST /dawnet
        response = self.client.post('/api/dawnet',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # PUT /dawnet/id
        response = self.client.put(f'/api/dawnet/dawnet_id',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DELETE /dawnet/id
        response = self.client.delete(f'/api/dawnet/dawnet_id',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST /dawnet/non-generic
        response = self.client.post(f'/api/dawnet/non-generic',
            data={'test': 'test'}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST ERROR /dawnet/non-generic
        response = self.client.post(f'/api/dawnet/non-generic',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
