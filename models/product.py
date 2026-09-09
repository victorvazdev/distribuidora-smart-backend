from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from models.base import Base


class Product(Base):
    '''Representa um produto no estoque.

    Esta entidade mapeia a tabela 'product' no banco de dados. Ela armazena os 
    detalhes comerciais e de estoque do produto.
    '''
    __tablename__ = 'product'

    id = Column('pk_product', Integer, primary_key=True)
    name = Column(String(100))
    barcode = Column(String(100), unique=True)
    quantity = Column(Integer)
    value = Column(Float)
    image_url = Column(String(255), nullable=True)
    insertion_date = Column(DateTime, default=datetime.now())

    def __init__(self, name:str, barcode:str, quantity:int, value:float, image_url:str, insertion_date:Union[DateTime, None] = None):
        '''Inicializa um novo registro do produto.

        Argumentos:
            name (str): Nome do produto.
            barcode (str): Código de barras do produto.
            quantity (int): Quantidade disponível no estoque.
            value (float): Preço do produto.
            image_url (str): Imagem do produto.
            insertion_date (DateTime, opcional): Data e hora em que o produto foi adicionado 
                ao sistema. Caso não seja informada, o sistema registrará o momento exato da criação.
        '''
        self.name = name
        self.barcode = barcode
        self.quantity = quantity
        self.value = value
        self.image_url = image_url

        # Caso a data de adição for informada, ela será configurada ao invés da data atual.
        if insertion_date:
            self.insertion_date = insertion_date            
