# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.data_source import DataSource  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.indexer import Indexer  # noqa: E501
from swagger_server.models.inline_response201 import InlineResponse201  # noqa: E501
from swagger_server.models.job import Job  # noqa: E501
from swagger_server.models.job_configuration import JobConfiguration  # noqa: E501
from swagger_server.models.record import Record  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_indexers_get(self):
        """Test case for indexers_get

        List all available indexers.
        """
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/indexers',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_indexers_indexer_type_data_sources_data_source_id_records_get(self):
        """Test case for indexers_indexer_type_data_sources_data_source_id_records_get

        List all records for a specific data source of an indexer
        """
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/indexers/{indexerType}/dataSources/{dataSourceId}/records'.format(indexer_type='indexer_type_example', data_source_id='data_source_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_indexers_indexer_type_data_sources_get(self):
        """Test case for indexers_indexer_type_data_sources_get

        List all data sources for a specific indexer type
        """
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/indexers/{indexerType}/dataSources'.format(indexer_type='indexer_type_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_jobs_get(self):
        """Test case for jobs_get

        List the jobs
        """
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/jobs',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_jobs_job_id_delete(self):
        """Test case for jobs_job_id_delete

        Delete a job
        """
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/jobs/{jobId}'.format(job_id='job_id_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_jobs_job_id_get(self):
        """Test case for jobs_job_id_get

        Get a job's details
        """
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/jobs/{jobId}'.format(job_id='job_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_jobs_post(self):
        """Test case for jobs_post

        Create a new job with a command or configuration
        """
        body = JobConfiguration()
        response = self.client.open(
            '/smartsawhuman/kb-indexer/1.0.0/jobs',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
