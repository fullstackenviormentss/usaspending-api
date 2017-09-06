import logging
import urllib
from urllib.error import HTTPError

from usaspending_api.awards.models import Award
from usaspending_api.common.exceptions import InvalidParameterException

logger = logging.getLogger(__name__)


def spending_filter(alt_set, queryset, filters, _type):

    for key, value in filters.items():
        # check for valid key
        if value is None:
            raise InvalidParameterException('Invalid filter: ' + key + ' has null as its value.')

        key_list = ['budget_function', 'budget_subfunction', 'federal_account', 'program_activity', 'object_class',
                    'recipient', 'award', 'award_category', 'agency', 'agency_top', 'agency_sub', 'fy']

        if key not in key_list:
            raise InvalidParameterException(
                key + ' filter does not exist.'
                      'Valid Filters: budget_function, budget_subfunction, federal_account,'
                      'program_activity, object_class, recipient, award, award_category,'
                      'agency, agency_top, agency_sub fy.')

        # budget_function - DONE
        if key == 'budget_function':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(treasury_account__budget_function_code=value)
            else:
                or_queryset = queryset.filter(treasury_account__budget_function_code=value)
            if or_queryset is not None:
                queryset &= or_queryset

        # budget_subfunction - DONE
        elif key == 'budget_subfunction':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(treasury_account__budget_subfunction_code=value)
            else:
                or_queryset = queryset.filter(treasury_account__budget_subfunction_code=value)
            if or_queryset is not None:
                queryset &= or_queryset

        # federal_account - DONE
        elif key == 'federal_account':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(treasury_account__federal_account__main_account_code=value)
            else:
                or_queryset = queryset.filter(treasury_account__federal_account__main_account_code=value)
            if or_queryset is not None:
                queryset &= or_queryset

        # program_activity - DONE
        elif key == 'program_activity':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(program_activity__program_activity_code=value)
            else:
                or_queryset = queryset.filter(program_activity__program_activity_code=value)
            if or_queryset is not None:
                queryset &= or_queryset

        # object_class - DONE
        elif key == 'object_class':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(object_class__major_object_class=value)
            else:
                or_queryset = queryset.filter(object_class__major_object_class=value)
            if or_queryset is not None:
                queryset &= or_queryset

        # recipient - DONE
        elif key == 'recipient':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(
                    treasury_account__in=alt_set.filter(
                        award__in=Award.objects.all().filter(
                           recipient__recipient_unique_id=value)).values_list('treasury_account_id', flat=True))
            else:
                or_queryset = queryset.filter(
                    treasury_account__in=alt_set.filter(
                        award__in=Award.objects.all().filter(
                           recipient__recipient_unique_id=value)).values_list('treasury_account_id', flat=True))
            if or_queryset is not None:
                queryset &= or_queryset

        # award - DONE
        elif key == 'award':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(
                    treasury_account__in=alt_set.filter(
                        award__in=Award.objects.all().filter(
                           piid=value)).values_list('treasury_account_id', flat=True))
            else:
                or_queryset = queryset.filter(
                    treasury_account__in=alt_set.filter(
                        award__in=Award.objects.all().filter(
                           piid=value)).values_list('treasury_account_id', flat=True))
            if or_queryset is not None:
                queryset &= or_queryset

        # award_category - DONE
        elif key == 'award_category':
            or_queryset = None
            if or_queryset:
                or_queryset |= or_queryset.filter(
                    treasury_account__in=alt_set.filter(
                        award__in=Award.objects.all().filter(
                           fain=value)).values_list('treasury_account_id', flat=True))
            else:
                or_queryset = queryset.filter(
                    treasury_account__in=alt_set.filter(
                        award__in=Award.objects.all().filter(
                           fain=value)).values_list('treasury_account_id', flat=True))
            if or_queryset is not None:
                queryset &= or_queryset

        # agency - DONE
        elif key == 'agency':
            or_queryset = None
            try:
                if or_queryset:
                    or_queryset |= or_queryset.filter(
                        treasury_account__awarding_toptier_agency__toptier_agency_id=value)
                else:
                    or_queryset = queryset.filter(
                        treasury_account__awarding_toptier_agency__toptier_agency_id=value)
                if or_queryset is not None:
                    queryset &= or_queryset
            except urllib.error.HTTPError:
                raise InvalidParameterException('Invalid agency ID: ' + value + ' does not exist.')
            finally:
                if or_queryset is not None:
                    queryset &= or_queryset

        # agency_top - DONE
        elif key == 'agency_top':
            or_queryset = None
            try:
                if or_queryset:
                    or_queryset |= or_queryset.filter(treasury_account__awarding_toptier_agency__cgac_code=value)
                else:
                    or_queryset = queryset.filter(treasury_account__awarding_toptier_agency__cgac_code=value)
                if or_queryset is not None:
                    queryset &= or_queryset
            except urllib.error.HTTPError:
                raise InvalidParameterException('Invalid top tier agency ID: ' + value + ' does not exist.')
            finally:
                if or_queryset is not None:
                    queryset &= or_queryset

        # agency_sub - DONE
        elif key == 'agency_sub':
            or_queryset = None
            try:
                if or_queryset:
                    or_queryset |= or_queryset.filter(
                        treasury_account__in=alt_set.filter(
                            award__in=Award.objects.all().filter(
                                awarding_agency__subtier_agency__subtier_code=value)
                        ).values_list('treasury_account_id', flat=True))
                else:
                    or_queryset = queryset.filter(
                        treasury_account__in=alt_set.filter(
                            award__in=Award.objects.all().filter(
                                awarding_agency__subtier_agency__subtier_code=value)
                        ).values_list('treasury_account_id', flat=True))
                if or_queryset is not None:
                    queryset &= or_queryset
            except urllib.error.HTTPError:
                raise InvalidParameterException('Invalid sub tier agency ID: ' + value + ' does not exist.')
            finally:
                if or_queryset is not None:
                    queryset &= or_queryset

    return queryset
