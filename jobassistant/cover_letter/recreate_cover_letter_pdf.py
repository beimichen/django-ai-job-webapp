import io
import random
import time

from jobassistant.dashboard.weasyprint_extended import CustomDocument, CustomHTML
from weasyprint import CSS
from weasyprint.fonts import FontConfiguration


def pdf_cover_letter_edit_from_dashboard(  # cover letter view
        environment,
        form_id,
        letter_in,
        user_first_name,
        user_middle_name,
        user_last_name,
        company_name,
        contact_name,
        position):
    # Initialize pdf layout

    version = random.randint(1, 1000000000)

    user_id = form_id

    stream = io.BytesIO()

    company_file_name = company_name.replace(" ", "_")

    if company_name:

        full_filename = company_file_name + "_updated_cover_letter_" + str(user_id) + "_" + str(version) + ".pdf"

    else:

        full_filename = "_updated_cover_letter_" + str(user_id) + ".pdf"


    Story = []


    # Date
    date = str(time.strftime("%d/%m/%Y"))

    ptext = ''


    # Contact + Company

    if contact_name.lower() != 'skip':
        ptext = '<p style=font-weight:bold;>{}</p>'.format(contact_name)
        Story.append(ptext)
    else:
        pass

    if company_name:
        ptext = '<p style=font-weight:bold;>{}</p>'.format(company_name)
        Story.append(ptext)
    else:
        pass


    # Body

    letter_seperated = letter_in.splitlines()

    cover_letter_text = ''
    for letter_component in letter_seperated:
        cover_letter_text += f'<p>{letter_component}</p>'

    fullname = user_first_name.capitalize() + user_last_name.capitalize()

    template = f"""
                        <html>
                            <head>
                            <title>{fullname} - Curriculum Vitae</title>

                            <link type="text/css" rel="stylesheet" href="style.css">
                            <link href='http://fonts.googleapis.com/css?family=Rokkitt:400,700|Lato:400,300' rel='stylesheet' type='text/css'>

                            </head>
                            <body class="page">
                            <div id="cv">
                                <div class="mainDetails">

                                    <div id="name">
                                        <h1>{fullname}</h1>
                                        <h2>{position.title()}</h2>
                                    </div>

                                    <div id="contactDetails">
                                        <ul>
                                            <li>{date}</li>
                                        </ul>
                                    </div>
                                    <div class="clear"></div>
                                </div>

                                <div id="mainArea">
                                    <section>
                                        <article>

                                            <div class="sectionCoverLetter">
                                                {cover_letter_text}
                                            </div>
                                        </article>
                                        <div class="clear"></div>
                                    </section>

                                </div>
                            </div>
                            </body>
                            </html>
                        """

    # Generate pdf and Upload to s3 using Weasyprint and boto3 respectively

    font_config = FontConfiguration()

    html = CustomHTML(string=template)

    css = [
        CSS(filename='./jobassistant/dashboard/weasyprint_css/style.css'),
    ]

    object_url = html.write_pdf_and_store_s3(
        full_filename,
        stylesheets=css,
        font_config=font_config,
        env_url=environment,
        data_type='coverletter'
    )

    return object_url
