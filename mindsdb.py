from typing import Any
from pydantic import BaseModel, Field
from requests import HTTPError
import mindsdb_sdk
import streamlit as st
from mindsdb_sdk.databases import Database
from langchain.output_parsers import PydanticOutputParser
from pandas import DataFrame

MINDSDB_HOST = "https://cloud.mindsdb.com"


class DataFeature(BaseModel):
    chartType: str = Field(
        ...,
        enum=["scatter_chart", "bar_chart", "area_chart", "line_chart"],
        description="""
        the chart type to visualize the dataframe strictly following rules:
        Use 'scatter_chart': if the dataframe contains categorical data many values with mixed types or if the  dataframe contains numerical data with multiple dimensions.

        Use 'scatter_chart' if the dataframe has more than 10 columns or if the dataframe has more than 3 diffrerent data types

        Use 'area_chart': if the dataframe is monthly-basis, daily-basis, or yearly-basis or if the dataframe shows changes over time, such as sales growth or customer churn or if dataframe shows comparisons between different categories.

        Use 'bar_chart': if the dataframe contains categorical data with related types, such as product categories or customer demographics or if the dataframe shows comparisons between different categories.

        Use 'line_chart': if the dataframe is seconds-basis or smaller periods, such as stock prices or website traffic or the dataframe shows comparisons between different categories.

        Use 'scatter_chart' if the data provided doesn't match any of the above criteria
     """,
    )
    column: str = Field(
        ...,
        description="""
        the column name in the dataframe that is best for the x-axis
        """,
    )


parser = PydanticOutputParser(pydantic_object=DataFeature)
parser_instructions = parser.get_format_instructions()


class MindsDB:
    """
    MindsDB manager class
    """

    def __init__(self, email: str, password: str) -> None:
        """
        initializer class.
        Args:
            email: MindsDB account email address (that is stored as an env var)
            password: MindsDB account password
        """
        self.email = email
        self.password = password
        self.file_db = None
        self.is_authenticated: bool = False
        self.database: Database
        self.server = None
        if not self.is_authenticated:
            self.authenticate()

    def authenticate(self) -> None:
        """
        authorizes the email and password with MindsDB's host
        """
        try:
            # self.server = mindsdb_sdk.connect(
            #     MINDSDB_HOST,
            #     login=self.email,
            #     password=self.password,
            # )
            self.server = mindsdb_sdk.connect("http://127.0.0.1:47334")
            self.file_db = self.server.databases.files
            print(self.file_db.tables.create)
        except HTTPError:
            raise Exception("Email or password is incorrect. Make sure to enter the right credentials.")
        except ConnectionError as e:
            raise Exception("Make sure you have access to the internet and try again.", e)

        self.is_authenticated = True

    def upload_file(self, filename, dataframe):
        if len(dataframe):
            self.file_db.tables.create(filename, dataframe, replace=True)

    def create_model(self, openai_api_key, temperature=0) -> Database:
        if self.server:
            # langchain_engine = self.server.langchain_engine
            prompt_template = "Answer the users input in a helpful way: {{input}}"
            query = self.server.query(
                f"""
                    CREATE MODEL IF NOT EXISTS ai_chart_agent
                    PREDICT completion
                    USING engine = 'langchain_engine',
                    model_name = 'openai',
                    openai_api_key = '{openai_api_key}',
                    temperature = '{temperature}',
                    prompt_template = '{prompt_template}';
                """
            )
        response = query.fetch()
        return response

    def predict_chart_type(self, filename):
        query = self.file_db.query(
            f"""
                SELECT input, completion
                FROM tool_based_agent
                WHERE input = 'Given a dataframe, {filename} {parser_instructions}'
                USING
                    verbose = True,
                    tools = [],
                    max_iterations = 10;
            """
        )
        res = query.fetch()
        return res
