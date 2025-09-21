# Product Management System

A Django-based RESTful API for managing products, users, and authentication. Includes JWT authentication, bulk product operations, change logging, and admin features.

## Features

- Product CRUD with bulk create and export
- Change logging for product updates and deletes
- JWT authentication (access/refresh tokens)
- Custom user model
- Admin interface
- CORS support
- Rate limiting
- Swagger/OpenAPI documentation

## Project Structure

```
app/
  auth_api/         # User authentication and management
  products/         # Product models, views, signals, serializers
  proj/             # Django project settings and static files
  utils/            # Configuration utilities
  .env              # Environment variables
  requirements.txt  # Python dependencies
```

## Setup

1. **Clone the repository**
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment**
   - Copy `.env` and set your secrets and DB config.
4. **Apply migrations**
   ```sh
   python proj/manage.py migrate
   ```
5. **Create superuser**
   ```sh
   python proj/manage.py createsuperuser
   ```
6. **Run server**
   ```sh
   python proj/manage.py runserver
   ```

## API Endpoints

- `/products/` - List & create products
- `/products/<uuid:pk>/` - Retrieve, update, delete product
- `/products/bulk-create/` - Bulk product creation
- `/products/export/` - Export products
- `/products/search/` - Search products

See [app/products/urls.py](app/products/urls.py) for details.

## Authentication

- JWT via `rest_framework_simplejwt`
- Custom user model: [app/auth_api/models.py](app/auth_api/models.py)
- Configure tokens in `.env` and [app/proj/proj/settings.py](app/proj/proj/settings.py)

## Change Logging

Product changes are tracked using Django signals:
- See [`track_product_changes`](app/products/signals.py), [`log_product_save`](app/products/signals.py), [`log_product_delete`](app/products/signals.py)
- Change logs stored in `ProductChangeLog` ([app/products/models.py](app/products/models.py))

## Environment Variables

See [app/.env](app/.env) for all configuration options.


## License

MIT

---

**For more details, see the source files:**
- [app/products/models.py](app/products/models.py)
- [app/products/serializers.py](app/products/serializers.py)
- [app/products/views.py](app/products/views.py)
- [app/auth_api/models.py](app/auth_api/models.py)
- [app/proj/proj/settings.py](app/proj/proj/settings.py)