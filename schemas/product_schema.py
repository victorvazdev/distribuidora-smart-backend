from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

from models.product import Product


class ProductSchema(BaseModel):
    '''Define como um novo produto deve ser representado para inserção no banco de dados.
    '''
    name: str = Field('AGUA MIN CRYSTAL S/GAS 500ML', description='Nome do produto.')
    barcode: str = Field('7894900530001', description='Código de barras do produto.')
    quantity: Optional[int] = Field(12, description='Quantidade disponível no estoque.')
    value: float = Field(2.50, description='Preço do produto.')
    image_url: str = Field('https://images.openfoodfacts.org/images/products/789/490/053/0001/front_pt.30.400.jpg', description='URL da imagem do produto.')

    @field_validator('name', 'barcode', mode='before')
    @classmethod
    def format_string_fields(cls, value):
        '''Converte vazios/null para None, e números para string.'''
        if value in ("", "null"):
            return None
        if isinstance(value, (int, float)):
            return str(value)
        return value

    @field_validator('quantity', 'value', mode='before')
    @classmethod
    def empty_to_none_numbers(cls, value):
        '''Converte apenas vazios/null para None nos campos numéricos.'''
        if value in ("", "null"):
            return None
        return value


class ProductListSchema(BaseModel):
    '''Define como uma listagem de vários produtos será retornada pela API.
    '''
    products: List[ProductSchema]


class ProductSearchSchema(BaseModel):
    '''Define a estrutura para busca parcial por nome ou código de barras.'''
    name: Optional[str] = Field(None, description='Nome parcial ou completo do produto.')
    barcode: Optional[str] = Field(None, description='Código de barras parcial ou completo.')


class ProductIdSchema(BaseModel):
    '''Define a estrutura para busca de um produto específico pelo ID.'''
    id: int = Field(description='ID do produto a ser buscado.')


class ProductBarcodeSchema(BaseModel):
    '''Define a estrutura para busca do primeiro produto correspondente a um código de barras.'''
    barcode: str = Field(description='Código de barras exato do produto a ser buscado.')


class ProductDeleteSchema(BaseModel):
    '''Define a estrutura dos dados necessários para realizar a exclusão de um produto.
    '''
    id: int = Field(description='ID do produto a ser deletado.')


class ProductUpdateSchema(BaseModel):
    '''Define como os dados de um produto devem ser enviados para permitir a sua atualização.
    '''
    id: int = Field(description='ID do produto a ser atualizado.')
    name: Optional[str] = Field(None, description='Novo nome do produto.')
    barcode: Optional[str] = Field(None, description='Novo código de barras do produto.')
    quantity: Optional[int] = Field(None, description='Nova quantidade disponível no estoque.')
    value: Optional[float] = Field(None, description='Novo preço do produto.')
    image_url: Optional[str] = Field(None, description='Nova url da imagem do produto.')

    @field_validator('name', 'barcode', mode='before')
    @classmethod
    def format_string_fields(cls, value):
        '''Converte vazios/null para None, e números para string.'''
        if value in ("", "null"):
            return None
        if isinstance(value, (int, float)):
            return str(value)
        return value

    @field_validator('quantity', 'value', mode='before')
    @classmethod
    def empty_to_none_numbers(cls, value):
        '''Converte apenas vazios/null para None nos campos numéricos.'''
        if value in ("", "null"):
            return None
        return value


def display_product(product: Product):
    '''Retorna uma representação em dicionário do objeto Product.
    '''
    return {
        'id': product.id,
        'name': product.name,
        'barcode': product.barcode,
        'quantity': product.quantity,
        'value': product.value,
        'image_url': product.image_url
    }


def display_product_list(products: List[Product]):
    '''Retorna uma representação em dicionário de uma lista de objetos Product, 
    formatando cada um para exibição adequada.
    '''
    product_list = []

    for product in products:
        product_list.append({
            'id': product.id,
            'name': product.name,
            'barcode': product.barcode,
            'quantity': product.quantity,
            'value': product.value,
            'image_url': product.image_url
        })

    return {'products': product_list}
