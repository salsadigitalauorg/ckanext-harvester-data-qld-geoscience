from behave import step
from behaving.personas.steps import *  # noqa: F401, F403
from behaving.web.steps import *  # noqa: F401, F403
from behaving.web.steps.url import when_i_visit_url
import email
import quopri
import random


@step(u'I get the current URL')
def get_current_url(context):
    context.browser.evaluate_script("document.documentElement.clientWidth")


@step(u'I go to homepage')
def go_to_home(context):
    when_i_visit_url(context, '/')


@step(u'I go to register page')
def go_to_register_page(context):
    context.execute_steps(u"""
        When I go to homepage
        And I click the link with text that contains "Register"
    """)


@step(u'I log in')
def log_in(context):
    assert context.persona
    context.execute_steps(u"""
        When I go to homepage
        And I click the link with text that contains "Log in"
        And I log in directly
    """)


@step(u'I log in directly')
def log_in_directly(context):
    """
    This differs to the `log_in` function above by logging in directly to a page where the user login form is presented
    :param context:
    :return:
    """

    assert context.persona
    context.execute_steps(u"""
        When I fill in "login" with "$name"
        And I fill in "password" with "$password"
        And I press the element with xpath "//button[contains(string(), 'Login')]"
        Then I should see an element with xpath "//a[@title='Log out']"
    """)


@step(u'I should see a login link')
def login_link_visible(context):
    context.execute_steps(u"""
        Then I should see an element with xpath "//h1[contains(string(), 'Login')]"
    """)


@step(u'I fill in title with random text')
def title_random_text(context):

    assert context.persona
    context.execute_steps(u"""
        When I fill in "title" with "Test Title {0}"
    """.format(random.randrange(1000)))


@step(u'I go to dataset page')
def go_to_dataset_page(context):
    when_i_visit_url(context, '/dataset')


@step(u'I go to dataset "{name}"')
def go_to_dataset(context, name):
    when_i_visit_url(context, '/dataset/' + name)


@step(u'I edit the "{name}" dataset')
def edit_dataset(context, name):
    when_i_visit_url(context, '/dataset/edit/{}'.format(name))


@step(u'I go to organisation page')
def go_to_organisation_page(context):
    when_i_visit_url(context, '/organization')


@step(u'I set persona var "{key}" to "{value}"')
def set_persona_var(context, key, value):
    context.persona[key] = value


@step(u'I log in and go to the data requests page')
def log_in_go_to_datarequest_page(context):
    assert context.persona
    context.execute_steps(u"""
        When I log in
        And I go to the data requests page
    """)


@step(u'I go to the data requests page')
def go_to_datarequest_page(context):
    when_i_visit_url(context, '/datarequest')


@step(u'I log in and create a datarequest')
def log_in_create_a_datarequest(context):
    assert context.persona
    context.execute_steps(u"""
        When I log in and go to the data requests page
        And I create a datarequest
    """)


@step(u'I create a datarequest')
def create_datarequest(context):

    assert context.persona
    context.execute_steps(u"""
        When I go to the data requests page
        And I click the link with text that contains "Add data request"
        And I fill in title with random text
        And I fill in "description" with "Test description"
        And I press the element with xpath "//button[contains(@class, 'btn-primary')]"
    """)


@step(u'I go to my reports page')
def go_to_reporting_page(context):
    when_i_visit_url(context, '/dashboard/reporting')


@step(u'I go to dataset "{name}" comments')
def go_to_dataset_comments(context, name):
    context.execute_steps(u"""
        When I go to dataset "%s"
        And I click the link with text that contains "Comments"
    """ % (name))


@step(u'I go to data request "{subject}"')
def go_to_data_request(context, subject):
    context.execute_steps(u"""
        When I go to the data requests page
        And I click the link with text "%s"
        Then I should see "%s" within 5 seconds
    """ % (subject, subject))


@step(u'I go to data request "{subject}" comments')
def go_to_data_request_comments(context, subject):
    context.execute_steps(u"""
        When I go to data request "%s"
        And I click the link with text that contains "Comments"
    """ % (subject))


@step(u'I submit a comment with subject "{subject}" and comment "{comment}"')
def submit_comment_with_subject_and_comment(context, subject, comment):
    """
    There can be multiple comment forms per page (add, edit, reply) each with fields named "subject" and "comment"
    This step overcomes a limitation of the fill() method which only fills a form field by name
    :param context:
    :param subject:
    :param comment:
    :return:
    """
    context.browser.execute_script(
        "document.querySelector('form#comment_form input[name=\"subject\"]').value = '%s';" % subject)
    context.browser.execute_script(
        "document.querySelector('form#comment_form textarea[name=\"comment\"]').value = '%s';" % comment)
    context.browser.execute_script(
        "document.querySelector('form#comment_form .form-actions input[type=\"submit\"]').click();")


@step(u'I submit a reply with comment "{comment}"')
def submit_reply_with_comment(context, comment):
    """
    There can be multiple comment forms per page (add, edit, reply) each with fields named "subject" and "comment"
    This step overcomes a limitation of the fill() method which only fills a form field by name
    :param context:
    :param comment:
    :return:
    """
    context.browser.execute_script(
        "document.querySelector('.comment-wrapper form textarea[name=\"comment\"]').value = '%s';" % comment)
    context.browser.execute_script(
        "document.querySelector('.comment-wrapper form .form-actions input[type=\"submit\"]').click();")


@step(u'I create a dataset with title "{title}"')
def create_dataset_titled(context, title):
    context.execute_steps(u"""
        When I visit "dataset/new"
        And I fill in "title" with "{title}"
        And I fill in "notes" with "Description"
        And I fill in "version" with "1.0"
        And I fill in "author_email" with "test@me.com"
        And I select "NO" from "de_identified_data"
        And I press "Add Data"
        And I execute the script "document.getElementById('field-image-url').value='https://example.com'"
        And I fill in "name" with "Test Resource"
        And I select "HTML" from "format"
        And I fill in "description" with "Test Resource Description"
        And I press "Finish"
    """.format(title=title))


@step(u'I create a dataset with license {license} and resource file {file}')
def create_dataset_json(context, license, file):
    create_dataset(context, license, 'JSON', file)


@step(u'I create a dataset with license {license} and {file_format} resource file {file}')
def create_dataset(context, license, file_format, file):
    assert context.persona
    context.execute_steps(u"""
        When I visit "dataset/new"
        And I fill in title with random text
        And I fill in "notes" with "Description"
        And I fill in "version" with "1.0"
        And I fill in "author_email" with "test@me.com"
        And I execute the script "document.getElementById('field-license_id').value={license}"
        Then I select "NO" from "de_identified_data"
        And I press "Add Data"
        And I attach the file {file} to "upload"
        And I fill in "name" with "Test Resource"
        And I execute the script "document.getElementById('field-format').value={file_format}"
        And I fill in "description" with "Test Resource Description"
        And I press "Finish"
    """.format(license=license, file=file, file_format=file_format))


# The default behaving step does not convert base64 emails
# Modified the default step to decode the payload from base64
@step(u'I should receive a base64 email at "{address}" containing "{text}"')
def should_receive_base64_email_containing_text(context, address, text):
    def filter_contents(mail):
        mail = email.message_from_string(mail)
        payload = mail.get_payload()
        payload += "=" * ((4 - len(payload) % 4) % 4)  # do fix the padding error issue
        payload_bytes = quopri.decodestring(payload)
        if len(payload_bytes) > 0:
            payload_bytes += b'='  # do fix the padding error issue
        decoded_payload = payload_bytes.decode('base64')
        print('decoded_payload: ', decoded_payload)
        return text in decoded_payload

    assert context.mail.user_messages(address, filter_contents)


@step(u'I log in and go to admin config page')
def log_in_go_to_admin_config(context):
    assert context.persona
    context.execute_steps(u"""
        When I log in
        And I go to admin config page
    """)


@step(u'I go to admin config page')
def go_to_admin_config(context):
    when_i_visit_url(context, '/ckan-admin/config')
