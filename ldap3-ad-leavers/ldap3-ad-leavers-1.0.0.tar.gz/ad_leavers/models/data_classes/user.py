from dataclasses import dataclass
from datetime import datetime, timedelta
from ad_leavers.models.core.object_class import ObjectClass

@dataclass
class User(ObjectClass):   

    def __init__(self, schema: dict):

        """
            This is the User data class model
            It inherits from the ObjectClass model
            This class will model a user object in an AD

        Parameters:
            schema (dict): The schema of an AD object that represent a User/Person from ldap3
        """     
        
        # * Extract necessary parameters
        self.sam_account_name = schema['attributes']['sAMAccountName']
        self.common_name = schema['attributes']['cn']
        self.display_name = schema['attributes'].get('displayName', None)
        self.email = schema['attributes'].get('mail', None)
        self.description = schema['attributes'].get('description', None)
        self.member_of = schema['attributes'].get('memberOf', None)
        self.user_principal_name = schema['attributes'].get('userPrincipalName', None)
        self.account_expires = schema['attributes'].get('accountExpires', None) if schema['raw_attributes']['accountExpires'][0] != b'0' else None

        # * Initialize the parent class
        super().__init__(
            name=schema['attributes']['name'], 
            distinguished_name=schema['attributes']['distinguishedName'], 
            when_created=schema['attributes']['whenCreated']
        )

    def __str__(self) -> str:
        return ','.join('%s=%s' % item for item in vars(self).items())

    def is_eligible_to_disable(self):

        """
            This function will verify if the user is eligible to have its account disabled
            Eligibility will be calculated whether the account has already expired or not
        Returns:
            bool: Returns True or False
        """        

        # * Verify if an expiration has been set on the account
        if self.account_expires:

            # * If the account has already expired, it is eligibe to be disabled
            return self.account_expires.replace(tzinfo=None) < datetime.today().replace(tzinfo=None)

        # * If there is not an expiration setup, the account is not eligible to be disabled
        return False

    def is_eligible_for_deletion(self, days_limit: int):

        """
            This function will verify if the user is eligible to have its account deleted
            Eligibility will be calculated whether the days_limit argument has already exceeded the
            date that the account has been expired

        Args:
            days_limit (int): The days after which an account is considered eligible to be deleted after it has been expired

        Returns:
            bool: Returns True or False
        """        

        # * Verify if an expiration has been set on the account
        if self.account_expires:

            # * Check whether the days limit has exceeded since the
            # * account was expired
            return (self.account_expires.replace(tzinfo=None) + timedelta(days=days_limit)) <= datetime.today().replace(tzinfo=None)
        
        # * If there is not an expiration setup, the account is not eligible for deletion
        return False