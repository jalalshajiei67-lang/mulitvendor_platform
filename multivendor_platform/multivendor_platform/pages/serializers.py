from rest_framework import serializers
from .models import AboutPage, ContactPage


class AboutPageSerializer(serializers.ModelSerializer):
    """
    Serializer for About Us page with multilingual and SEO fields
    """
    class Meta:
        model = AboutPage
        fields = [
            'id',
            # Persian Content
            'title_fa',
            'content_fa',
            # English Content
            'title_en',
            'content_en',
            # Persian SEO
            'meta_title_fa',
            'meta_description_fa',
            'meta_keywords_fa',
            # English SEO
            'meta_title_en',
            'meta_description_en',
            'meta_keywords_en',
            # Timestamps
            'updated_at',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactPageSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact Us page with multilingual and SEO fields
    """
    class Meta:
        model = ContactPage
        fields = [
            'id',
            # Persian Content
            'title_fa',
            'content_fa',
            'address_fa',
            'working_hours_fa',
            # Contact Information
            'phone',
            'email',
            # English Content
            'title_en',
            'content_en',
            'address_en',
            'working_hours_en',
            # Persian SEO
            'meta_title_fa',
            'meta_description_fa',
            'meta_keywords_fa',
            # English SEO
            'meta_title_en',
            'meta_description_en',
            'meta_keywords_en',
            # Timestamps
            'updated_at',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

