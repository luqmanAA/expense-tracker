from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django_auth_adfs.backend import AdfsAuthCodeBackend, logger
from django_auth_adfs.config import settings


class CustomADFSAuthCodeBackend(AdfsAuthCodeBackend):

    """
        Sub-class for AdfsAuthCodeBackend to provide different implementation
         of the create_user() method
    """

    def create_user(self, claims):
        """
        Create the user if it doesn't exist yet

        Args:
            claims (dict): claims from the access token

        Returns:
            django.contrib.auth.models.User: A Django user
        """
        # Create the user
        username_claim = settings.USERNAME_CLAIM
        guest_username_claim = settings.GUEST_USERNAME_CLAIM
        usermodel = get_user_model()

        iss = claims.get('iss')
        idp = claims.get('idp', iss)
        if (
                guest_username_claim
                and not claims.get(username_claim)
                and not settings.BLOCK_GUEST_USERS
                and (claims.get('tid') != settings.TENANT_ID or iss != idp)
        ):
            username_claim = guest_username_claim

        if not claims.get(username_claim):
            logger.error("User claim's doesn't have the claim '%s' in his claims: %s" %
                         (username_claim, claims))
            raise PermissionDenied

        """
            Incase Azure user does not have given_name and family_name (optional fields for Azure)
            Split whatever is set as display name on Azure (required field) at space and use as given_name and
            family name
        """
        if not claims.get('given_name') and not claims.get('family_name'):
            name = claims['name'].split()
            if len(name) > 1:
                claims['family_name'] = name[1]

            claims['given_name'] = name[0]

        userdata = {usermodel.USERNAME_FIELD: claims[username_claim].lower()}

        try:
            user = usermodel.objects.get(**userdata)

        except usermodel.DoesNotExist:
            if settings.CREATE_NEW_USERS:
                user = usermodel.objects.create(**userdata)
                logger.debug("User '%s' has been created.", claims[username_claim])
            else:
                logger.debug("User '%s' doesn't exist and creating users is disabled.", claims[username_claim])
                raise PermissionDenied
        if not user.password:
            user.set_unusable_password()

        return user
