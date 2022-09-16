from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_invitation(to_email, code, team):
    from_email = settings.DEFAULT_EMAIL_FROM
    acceptation_url = settings.ACCEPTATION_URL
    
    subject = 'Приглашение'
    text_content = 'Ваш код: %s' % code
    html_content = render_to_string(
        'users/email_invitation.html', 
        {
            'code': code, 
            'team': team,
            'acceptation_url': acceptation_url
        }
        )
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    
def send_invitation_accepted(team, invitation, to_email):
    from_email = settings.DEFAULT_EMAIL_FROM
    subject = 'Приглашение принято'
    text_content = 'Ваше приглашение было принято'
    html_content = render_to_string(
        'users/email_accepted_invitation.html',
        {
            'team': team,
            'invitation': invitation
        }
        )
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()