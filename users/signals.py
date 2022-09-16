from .models import Profile, CustomUser, Team, Relationship
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               full_name=instance.full_name,
                               phone_number=instance.phone_number,
                               date_birth=instance.date_birth,
                               email=instance.email
                               )
        
        
@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
@receiver(post_save, sender=Relationship)
def post_save_add_to_team(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    to_team = instance.to_team
    if instance.status == "accepted":
        to_team.members.add(receiver_.user)
        receiver_.teams.add(to_team)
        to_team.save()
        receiver_.save()