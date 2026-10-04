from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from textblob import TextBlob

_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            import spacy
            _nlp = spacy.load('en_core_web_sm')
        except OSError:
            _nlp = None
    return _nlp

class Entry(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class DailyTask(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Goal(models.Model):
    CATEGORY_CHOICES = [('personal', 'Personal'), ('career', 'Career'), ('health', 'Health'), ('education', 'Education'), ('other', 'Other')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='personal')
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PointedJournal(models.Model):
    CATEGORY_CHOICES = [('reflection', 'Reflection'), ('idea', 'Idea'), ('quote', 'Quote'), ('memory', 'Memory'), ('other', 'Other')]
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='reflection')
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class DailyTracker(models.Model):
    date = models.DateField(default=timezone.now)
    completed_tasks = models.IntegerField(default=0)
    pending_tasks = models.IntegerField(default=0)
    productivity_score = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        unique_together = ['date', 'user']

    def __str__(self):
        return f'Tracker for {self.date}'

class Vent(models.Model):
    SENTIMENT_CHOICES = [('very_positive', 'Very Positive'), ('positive', 'Positive'), ('neutral', 'Neutral'), ('negative', 'Negative'), ('very_negative', 'Very Negative')]
    MOOD_CHOICES = [('joy', 'Joy'), ('sadness', 'Sadness'), ('anger', 'Anger'), ('fear', 'Fear'), ('anxiety', 'Anxiety'), ('calm', 'Calm'), ('neutral', 'Neutral')]
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentiment_score = models.FloatField(default=0.0)
    sentiment_category = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='neutral')
    subjectivity_score = models.FloatField(default=0.0)
    key_phrases = models.JSONField(default=list, blank=True)
    detected_mood = models.CharField(max_length=20, choices=MOOD_CHOICES, default='neutral')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def analyze_sentiment(self):
        blob = TextBlob(self.content)
        self.sentiment_score = blob.sentiment.polarity
        self.subjectivity_score = blob.sentiment.subjectivity

        if self.sentiment_score >= 0.5:
            self.sentiment_category = 'very_positive'
        elif self.sentiment_score > 0:
            self.sentiment_category = 'positive'
        elif self.sentiment_score == 0:
            self.sentiment_category = 'neutral'
        elif self.sentiment_score > -0.5:
            self.sentiment_category = 'negative'
        else:
            self.sentiment_category = 'very_negative'

        if self.sentiment_score >= 0.5:
            self.detected_mood = 'joy'
        elif self.sentiment_score > 0:
            self.detected_mood = 'calm'
        elif self.sentiment_score == 0:
            self.detected_mood = 'neutral'
        elif self.sentiment_score > -0.5:
            self.detected_mood = 'sadness'
        else:
            self.detected_mood = 'anger'

        self.key_phrases = [phrase for phrase in blob.noun_phrases]

    def save(self, *args, **kwargs):
        self.analyze_sentiment()
        super().save(*args, **kwargs)
