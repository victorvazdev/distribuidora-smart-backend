import math

from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

from models import Session
from models.product import Product
from schemas.product_schema import *
from schemas.error_schema import ErrorSchema

product_tag = Tag(name='product', description='Gerenciamento de produtos.')
product_bp = APIBlueprint('product', __name__, abp_tags=[product_tag])


@product_bp.post('/product', tags=[product_tag], responses={'201': ProductSchema, '409': ErrorSchema, '400': ErrorSchema})
def add_product(form: ProductSchema):
    '''Cadastra um novo produto no estoque.
    
    Adiciona o produto com seus respectivos dados de nome, código de barras, 
    quantidade e valor no banco de dados.
    '''
    session = Session()

    try:
        product = Product(
            name=form.name,
            barcode=form.barcode,
            quantity=form.quantity,
            value=form.value,
            image_url=form.image_url
        )

        session.add(product)
        session.commit()
        return display_product(product), 201
    
    except IntegrityError:
        session.rollback()
        return {'message': f'Já existe um produto cadastrado com o código de barras {form.barcode}.'}, 409
    except Exception as e:
        session.rollback()
        return {'message': str(e)}, 400
    finally:
        session.close()


@product_bp.get('/products', tags=[product_tag], responses={'200': ProductListSchema, '404': ErrorSchema})
def get_products(query: PaginationQuerySchema):
    '''Lista todos os produtos cadastrados no estoque.
    
    Retorna os detalhes de todos os produtos registrados. 
    Retorna uma lista vazia caso o estoque não tenha produtos.
    '''
    session = Session()
    try:
        total_items = session.query(Product).count()
        total_pages = math.ceil(total_items / query.limit) if total_items > 0 else 1
        
        offset = (query.page - 1) * query.limit
        products = session.query(Product).limit(query.limit).offset(offset).all()

        if not products:
            return {'products': []}, 200
        else:
            return display_product_list(products, total_items, total_pages, query.page), 200
    finally:
        session.close()


@product_bp.get('/product/search', tags=[product_tag], responses={'200': ProductListSchema, '404': ErrorSchema})
def search_products(query: ProductSearchSchema):
    '''Busca produtos por similaridade de nome OU código de barras.
    
    Retorna uma lista de produtos que contenham o termo pesquisado no nome 
    ou no código de barras.
    '''
    session = Session()

    try:
        filters = []
        if query.name:
            filters.append(Product.name.ilike(f'%{query.name}%'))
        if query.barcode:
            filters.append(Product.barcode.ilike(f'%{query.barcode}%'))

        db_query = session.query(Product)

        if filters:
                    db_query = db_query.filter(or_(*filters))
        
        total_items = db_query.count()
        total_pages = math.ceil(total_items / query.limit) if total_items > 0 else 1
        offset = (query.page - 1) * query.limit
        products = db_query.limit(query.limit).offset(offset).all()

        if not products:
            return {'products': []}, 200
        
        return display_product_list(products, total_items, total_pages, query.page), 200
    finally:
        session.close()


@product_bp.get('/product', tags=[product_tag], responses={'200': ProductSchema, '404': ErrorSchema})
def get_product_by_id(query: ProductIdSchema):
    '''Busca os detalhes de um produto específico pelo seu ID.
    '''
    session = Session()

    try:
        product = session.query(Product).filter(Product.id == query.id).first()

        if not product:
            return {'message': f'O produto de ID {query.id} não foi encontrado.'}, 404
        
        return display_product(product), 200
    finally:
        session.close()


@product_bp.get('/product/barcode', tags=[product_tag], responses={'200': ProductSchema, '404': ErrorSchema})
def get_product_by_barcode(query: ProductBarcodeSchema):
    '''Busca o primeiro produto correspondente a um código de barras específico.
    
    Retorna os detalhes do primeiro produto encontrado no banco de dados 
    que possua a correspondência exata do código de barras informado.
    '''
    session = Session()

    try:
        product = session.query(Product).filter(Product.barcode == query.barcode).first()

        if not product:
            return {'message': f'Nenhum produto encontrado com o código de barras {query.barcode}.'}, 404
        
        return display_product(product), 200
    finally:
        session.close()

  
@product_bp.delete('/product', tags=[product_tag], responses={'200': ProductDeleteSchema, '404': ErrorSchema})
def delete_product(query: ProductDeleteSchema):
    '''Remove um produto do estoque.
    
    Busca o produto pelo seu ID e realiza a exclusão no banco de dados. 
    Retorna erro 404 caso o ID fornecido não seja encontrado.
    '''
    session = Session()

    try:
        db_query = session.query(Product)
        db_query = db_query.filter(Product.id == query.id)
        product = db_query.first()
        
        if not product:
            return {'message': f'O produto de ID {query.id} não foi encontrado.'}, 404

        product_name = product.name
        product_barcode = product.barcode
        
        product_deleted = db_query.delete()
        session.commit()

        if product_deleted:
            return {'message': f'Produto {product_name} (Código: {product_barcode}) foi removido com sucesso'}, 200
    finally:
        session.close()
    

@product_bp.put('/update_product', tags=[product_tag], responses={'200': ProductSchema, '404': ErrorSchema, '409': ErrorSchema})
def update_product(form: ProductUpdateSchema):
    '''Atualiza os dados de um produto existente.
    
    Busca o produto pelo ID e atualiza os campos fornecidos.
    Retorna erro 404 caso o produto não seja encontrado.
    '''
    session = Session()

    try:
        db_query = session.query(Product)
        db_query = db_query.filter(Product.id == form.id)
        product = db_query.first()

        if not product:
            return {'message': f'O produto de ID {form.id} não foi encontrado.'}, 404

        product.name = form.name if form.name is not None else product.name
        product.barcode = form.barcode if form.barcode is not None else product.barcode
        product.quantity = form.quantity if form.quantity is not None else product.quantity
        product.value = form.value if form.value is not None else product.value
        product.image_url = form.image_url if form.image_url is not None else product.image_url

        session.commit()
        return display_product(product), 200
    
    except IntegrityError:
        session.rollback()
        return {'message': f'O código de barras {form.barcode} já está em uso por outro produto.'}, 409
    except Exception as e:
        session.rollback()
        return {'message': f'Erro ao atualizar: {str(e)}'}, 400
    finally:
        session.close()
