# Dependency Injection Container for VLE User Management System
# Decision: Use dependency injection to decouple services and improve testability
# This follows the modular monolith pattern from the architecture document

from dependency_injector import containers, providers

class ApplicationContainer(containers.DeclarativeContainer):
    """Application DI container for service dependencies"""
    
    # Configuration provider
    # Decision: Centralize configuration access through DI container
    config = providers.Configuration()
    
    # Services will be defined in each feature module
    # Decision: Keep services modular while maintaining single container