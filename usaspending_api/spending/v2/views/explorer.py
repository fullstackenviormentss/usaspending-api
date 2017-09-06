from django.db.models import F, Sum, Value, CharField


class Explorer(object):
    def __init__(self, alt_set, queryset):
        self.alt_set = alt_set
        self.queryset = queryset

    def budget_function(self):
        # Budget Function Queryset
        queryset = self.queryset.annotate(
            id=F('treasury_account__budget_function_code'),
            type=Value('budget_function', output_field=CharField()),
            name=F('treasury_account__budget_function_title'),
            code=F('treasury_account__budget_function_code'),
        ).values('id', 'type', 'name', 'code', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def budget_subfunction(self):
        # Budget Sub Function Queryset
        queryset = self.queryset.annotate(
            id=F('treasury_account__budget_subfunction_code'),
            type=Value('budget_subfunction', output_field=CharField()),
            name=F('treasury_account__budget_subfunction_title'),
            code=F('treasury_account__budget_subfunction_code')
        ).values('id', 'type', 'name', 'code', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def federal_account(self):
        # Federal Account Queryset
        queryset = self.queryset.annotate(
            id=F('treasury_account__federal_account__main_account_code'),
            type=Value('federal_account', output_field=CharField()),
            name=F('treasury_account__federal_account__account_title'),
            code=F('treasury_account__federal_account__main_account_code')
        ).values(
            'id', 'type', 'name', 'code', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def program_activity(self):
        # Program Activity Queryset
        queryset = self.queryset.annotate(
            id=F('program_activity__program_activity_code'),
            type=Value('program_activity', output_field=CharField()),
            name=F('program_activity__program_activity_name'),
            code=F('program_activity__program_activity_code')
        ).values(
            'id', 'type', 'name', 'code', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def object_class(self):
        # Object Classes Queryset
        queryset = self.queryset.annotate(
            id=F('object_class__major_object_class'),
            type=Value('object_class', output_field=CharField()),
            name=F('object_class__major_object_class_name'),
            code=F('object_class__major_object_class')
        ).values(
            'id', 'type', 'name', 'code', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def recipient(self):
        # Recipients Queryset
        queryset = self.alt_set.annotate(
            id=F('award__recipient__recipient_unique_id'),
            type=Value('recipient', output_field=CharField()),
            name=F('award__recipient__recipient_name'),
            code=F('award__recipient__recipient_unique_id')
        ).values('id', 'type', 'name', 'code', 'amount').annotate(
            total=Sum('transaction_obligated_amount')).order_by('-total')

        return queryset

    def agency(self):
        # Awarding Agencies Queryset
        queryset = self.queryset.annotate(
            id=F('treasury_account__awarding_toptier_agency__toptier_agency_id'),
            type=Value('agency', output_field=CharField()),
            name=F('treasury_account__awarding_toptier_agency__name'),
            code=F('treasury_account__awarding_toptier_agency__toptier_agency_id')
        ).values('id', 'type', 'code', 'name', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def awarding_top_tier_agency(self):
        # Awarding Top Tier Agencies Queryset
        queryset = self.queryset.annotate(
            id=F('treasury_account__awarding_toptier_agency__cgac_code'),
            type=Value('top_tier_agency', output_field=CharField()),
            name=F('treasury_account__awarding_toptier_agency__name'),
            code=F('treasury_account__awarding_toptier_agency__cgac_code')
        ).values('id', 'type', 'code', 'name', 'amount').annotate(
            total=Sum('obligations_incurred_by_program_object_class_cpe')).order_by('-total')

        return queryset

    def awarding_sub_tier_agency(self):
        # Awarding Sub Tier Agencies Queryset
        queryset = self.alt_set.annotate(
            id=F('award__awarding_agency__subtier_agency__subtier_code'),
            type=Value('sub_tier_agency', output_field=CharField()),
            name=F('award__awarding_agency__subtier_agency__name'),
            code=F('award__awarding_agency__subtier_agency__subtier_code')
        ).values('id', 'type', 'code', 'name', 'amount').annotate(
            total=Sum('transaction_obligated_amount')).order_by('-total')

        return queryset

    def award_category(self):
        # Award Category Queryset
        queryset = self.alt_set.annotate(
            id=F('award__fain'),
            type=Value('award_category', output_field=CharField()),
            name=F('award__category'),
            code=F('award__fain')
        ).values('id', 'type', 'code', 'name', 'amount').annotate(
            total=Sum('transaction_obligated_amount')).order_by('-total')

        return queryset

    def award(self):
        # Awards Queryset
        queryset = self.alt_set.annotate(
            id=F('award__piid'),
            type=Value('award', output_field=CharField()),
            name=F('award__type_description'),
            code=F('award__piid')
        ).values('id', 'type', 'code', 'name', 'amount').annotate(
            total=Sum('transaction_obligated_amount')).order_by('-total')

        return queryset
