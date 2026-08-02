from flask import jsonify
from src.exceptions import AuthenticationError, AuthorizationError, ValidationError, NotFoundError, BusinessError


def register_error_handlers(app):
    """Register application-level error handlers."""

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({'error': 'validation_error', 'message': str(error)}), 400

    @app.errorhandler(AuthenticationError)
    def handle_auth_error(error):
        return jsonify({'error': 'authentication_error', 'message': str(error)}), 401

    @app.errorhandler(AuthorizationError)
    def handle_authz_error(error):
        return jsonify({'error': 'authorization_error', 'message': str(error)}), 403

    @app.errorhandler(NotFoundError)
    def handle_not_found(error):
        return jsonify({'error': 'not_found', 'message': str(error)}), 404

    @app.errorhandler(BusinessError)
    def handle_business_error(error):
        return jsonify({'error': 'business_error', 'message': str(error)}), 422

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        return jsonify({'error': 'internal_error', 'message': 'An unexpected error occurred.'}), 500
