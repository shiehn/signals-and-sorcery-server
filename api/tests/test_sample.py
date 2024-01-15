'''Test the stability of the API'''
from rest_framework import status
from rest_framework.test import APITestCase


class SampleTests(APITestCase):
    '''API Sample Tests'''

    def setUp(self) -> None:
        '''Setup the client to contact the API'''
        self.headers = {
            'Content-Type': 'application/json',
            'Accept-Language': 'fr'
        }


    def test_sample(self) -> None:
        '''Test the sample API'''
        # GET /sample
        response = self.client.get('/api/sample',
            headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # GET /sample/id
        response = self.client.get(f'/api/sample/sample_id',
            headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST /sample
        response = self.client.post('/api/sample',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # PUT /sample/id
        response = self.client.put(f'/api/sample/sample_id',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # DELETE /sample/id
        response = self.client.delete(f'/api/sample/sample_id',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST /sample/non-generic
        response = self.client.post(f'/api/sample/non-generic',
            data={'test': 'test'}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # POST ERROR /sample/non-generic
        response = self.client.post(f'/api/sample/non-generic',
            data={}, headers=self.headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
