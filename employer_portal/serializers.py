from rest_framework import serializers
from employer_portal.models import *



class JobDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = JobDetails
		fields = '__all__'



class JobRequirementsSerializer(serializers.ModelSerializer):
	class Meta:
		model = JobRequirements
		fields = '__all__'


class CompensationDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = CompensationDetails
		fields = '__all__'


class ApplicationDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = ApplicationDetails
		fields = '__all__'
