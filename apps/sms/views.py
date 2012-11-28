"""
                   GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.


  This version of the GNU Lesser General Public License incorporates
the terms and conditions of version 3 of the GNU General Public
License, supplemented by the additional permissions listed below.

  0. Additional Definitions.

  As used herein, "this License" refers to version 3 of the GNU Lesser
General Public License, and the "GNU GPL" refers to version 3 of the GNU
General Public License.

  "The Library" refers to a covered work governed by this License,
other than an Application or a Combined Work as defined below.

  An "Application" is any work that makes use of an interface provided
by the Library, but which is not otherwise based on the Library.
Defining a subclass of a class defined by the Library is deemed a mode
of using an interface provided by the Library.

  A "Combined Work" is a work produced by combining or linking an
Application with the Library.  The particular version of the Library
with which the Combined Work was made is also called the "Linked
Version".

  The "Minimal Corresponding Source" for a Combined Work means the
Corresponding Source for the Combined Work, excluding any source code
for portions of the Combined Work that, considered in isolation, are
based on the Application, and not on the Linked Version.

  The "Corresponding Application Code" for a Combined Work means the
object code and/or source code for the Application, including any data
and utility programs needed for reproducing the Combined Work from the
Application, but excluding the System Libraries of the Combined Work.

  1. Exception to Section 3 of the GNU GPL.

  You may convey a covered work under sections 3 and 4 of this License
without being bound by section 3 of the GNU GPL.

  2. Conveying Modified Versions.

  If you modify a copy of the Library, and, in your modifications, a
facility refers to a function or data to be supplied by an Application
that uses the facility (other than as an argument passed when the
facility is invoked), then you may convey a copy of the modified
version:

   a) under this License, provided that you make a good faith effort to
   ensure that, in the event an Application does not supply the
   function or data, the facility still operates, and performs
   whatever part of its purpose remains meaningful, or

   b) under the GNU GPL, with none of the additional permissions of
   this License applicable to that copy.

  3. Object Code Incorporating Material from Library Header Files.

  The object code form of an Application may incorporate material from
a header file that is part of the Library.  You may convey such object
code under terms of your choice, provided that, if the incorporated
material is not limited to numerical parameters, data structure
layouts and accessors, or small macros, inline functions and templates
(ten or fewer lines in length), you do both of the following:

   a) Give prominent notice with each copy of the object code that the
   Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the object code with a copy of the GNU GPL and this license
   document.

  4. Combined Works.

  You may convey a Combined Work under terms of your choice that,
taken together, effectively do not restrict modification of the
portions of the Library contained in the Combined Work and reverse
engineering for debugging such modifications, if you also do each of
the following:

   a) Give prominent notice with each copy of the Combined Work that
   the Library is used in it and that the Library and its use are
   covered by this License.

   b) Accompany the Combined Work with a copy of the GNU GPL and this license
   document.

   c) For a Combined Work that displays copyright notices during
   execution, include the copyright notice for the Library among
   these notices, as well as a reference directing the user to the
   copies of the GNU GPL and this license document.

   d) Do one of the following:

       0) Convey the Minimal Corresponding Source under the terms of this
       License, and the Corresponding Application Code in a form
       suitable for, and under terms that permit, the user to
       recombine or relink the Application with a modified version of
       the Linked Version to produce a modified Combined Work, in the
       manner specified by section 6 of the GNU GPL for conveying
       Corresponding Source.

       1) Use a suitable shared library mechanism for linking with the
       Library.  A suitable mechanism is one that (a) uses at run time
       a copy of the Library already present on the user's computer
       system, and (b) will operate properly with a modified version
       of the Library that is interface-compatible with the Linked
       Version.

   e) Provide Installation Information, but only if you would otherwise
   be required to provide such information under section 6 of the
   GNU GPL, and only to the extent that such information is
   necessary to install and execute a modified version of the
   Combined Work produced by recombining or relinking the
   Application with a modified version of the Linked Version. (If
   you use option 4d0, the Installation Information must accompany
   the Minimal Corresponding Source and Corresponding Application
   Code. If you use option 4d1, you must provide the Installation
   Information in the manner specified by section 6 of the GNU GPL
   for conveying Corresponding Source.)

  5. Combined Libraries.

  You may place library facilities that are a work based on the
Library side by side in a single library together with other library
facilities that are not Applications and are not covered by this
License, and convey such a combined library under terms of your
choice, if you do both of the following:

   a) Accompany the combined library with a copy of the same work based
   on the Library, uncombined with any other library facilities,
   conveyed under the terms of this License.

   b) Give prominent notice with the combined library that part of it
   is a work based on the Library, and explaining where to find the
   accompanying uncombined form of the same work.

  6. Revised Versions of the GNU Lesser General Public License.

  The Free Software Foundation may publish revised and/or new versions
of the GNU Lesser General Public License from time to time. Such new
versions will be similar in spirit to the present version, but may
differ in detail to address new problems or concerns.

  Each version is given a distinguishing version number. If the
Library as you received it specifies that a certain numbered version
of the GNU Lesser General Public License "or any later version"
applies to it, you have the option of following the terms and
conditions either of that published version or of any later version
published by the Free Software Foundation. If the Library as you
received it does not specify a version number of the GNU Lesser
General Public License, you may choose any version of the GNU Lesser
General Public License ever published by the Free Software Foundation.

  If the Library as you received it specifies that a proxy can decide
whether future versions of the GNU Lesser General Public License shall
apply, that proxy's public statement of acceptance of any version is
permanent authorization for you to choose that version for the
Library.
"""


import random

from django.conf import settings

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from sms.models import SMS, RES_UNKNOWN, RES_NUMBER_CONFIRMATION, RES_UNSUBSCRIBE
from sms.models import ACK_NUMBER_CONFIRMATION, ACK_UNSUBSCRIBE, ACK_JOB_APPLY, ACK_UNKNOWN
from sms.forms import ReceiveSMSForm
from applicant.models import ApplicantProfile, ApplicantJob
from job.models import Job
from job_recommendation.models import JobRecommendation

sms_templates = {
                 ACK_NUMBER_CONFIRMATION: 'sms/ack/number_confirmation.html',
                 ACK_UNSUBSCRIBE: 'sms/ack/unsubscribe.html',
                 ACK_JOB_APPLY: 'sms/ack/job_apply.html',
                 ACK_UNKNOWN: 'sms/ack/unknown.html',
                 }

@csrf_exempt
def receive_sms(request, template=None, form_class=ReceiveSMSForm):
    if request.method == 'POST':
        fields = request.POST
    else:
        fields = request.GET

    form = form_class(fields)
    context = {}
    if form.is_valid():
        profile = None
        try:
            profile = ApplicantProfile.objects.get(mobile_number=form.cleaned_data['From'])
            
        except ApplicantProfile.DoesNotExist:
            pass

        message = form.cleaned_data['Body']

        response, message_type = SMS.get_message_type(message, profile)
        context['response'] = response

        sms = SMS(applicant=profile, 
                  sent_by_us=False,
                  message=form.cleaned_data['Body'],
                  sms_sid=form.cleaned_data['SmsSid'],
                  phone_number=form.cleaned_data['From'],
                  message_type=message_type)

        sms.save()

        if profile is not None:
            if message_type == RES_NUMBER_CONFIRMATION:
                profile.confirmed_phone = True
                profile.save()
            
            if message_type == RES_UNSUBSCRIBE:
                profile.confirmed_phone = False
                profile.save()

        additional_context, template = handle_ack(response, message_type, profile)
        context.update(additional_context)
        
    return render_to_response(template,
                              context,
                              context_instance=RequestContext(request))

# Handle the specific acknowledgments to responses sent via text
# by applicants
def handle_ack(response, message_type, profile):
    # Acks are one value higher than the response
    additional_context = sms_ack_functions[message_type+1](response, profile)
    return additional_context, sms_templates[message_type+1]

# Send acknowledgment about phone number confirmation
def do_number_confirm(response, profile):
    pin = None
    if profile is not None:
        profile.confirmed_phone = True
        profile.save()

        user = profile.user
        if getattr(settings, 'DEMO_ENABLED', False):
            pin = '1234'
        else:
            pin = '%d' % (random.randint(0, 8999) + 1000)
        user.set_password(pin)
        user.is_active = True
        user.save()

        if getattr(settings, 'DEMO_ENABLED', False):
            setup_demo_user(profile)
    return { 'pin': pin }

# Send acknowledgment about unsubscribe
def do_unsubscribe(response, profile):
    if profile is not None:
        profile.confirmed_phone = False
        profile.save()

    return {}

# Send acknowledgment about job application being sent
def do_job_apply(response, profile):
    try:
        job = Job.objects.get(job_code=response)
        applications = ApplicantJob.objects.filter(job=job, applicant=profile)
        if applications.count() == 0:
            application = ApplicantJob(job=job, applicant=profile)
            application.save()
    except Job.DoesNotExist:
        job = None

    return { 'job': job }

# Send acknowledgment about unknown message coming through
def do_unknown(response, profile):
    return {}

sms_ack_functions = {
                     ACK_NUMBER_CONFIRMATION: do_number_confirm,
                     ACK_UNSUBSCRIBE: do_unsubscribe,
                     ACK_JOB_APPLY: do_job_apply,
                     ACK_UNKNOWN: do_unknown,
                     }


def setup_demo_user(profile):
    try:
        jobs = Job.objects.all().filter(pk__lte=10).order_by('?')[0:2]
        for job in jobs:
            recommendation = JobRecommendation(job=job,
                                               applicant=profile)
            recommendation.save()
    except:
        pass
