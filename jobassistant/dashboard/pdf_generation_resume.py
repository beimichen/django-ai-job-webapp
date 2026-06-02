from difflib import SequenceMatcher
import operator
import string
import random

from tools import *
from jobassistant.dashboard.weasyprint_extended import CustomDocument, CustomHTML
from weasyprint import CSS
from weasyprint.fonts import FontConfiguration


def gen_version_number(number_length):
    """Generate a random string of letters and digits """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(number_length))


def resume_order(position, industry, experience):

    env_url, admin, password, bucket = check_environment()

    file_name = 'industries.json'
    s3_file = bucket.Object(file_name)
    industries = fetch_data_from_s3_file(s3_file)

    data = industries

    included_past_positions = []

    # check if position has an industry that matches one of our "related industries", hence checking
    # whether it should be included in the resume

    for i in experience:

        industry_lookup = None

        try:
            industry_lookup = data[i["industry_name"]]

        except Exception as e:
            print(e)

        if industry_lookup:

            related_industries = industry_lookup["related_industries"]

            if industry in related_industries:
                included_past_positions.append([i["id"], i["position_name"]])

    list_of_similar_positions = []

    print(included_past_positions)

    if included_past_positions:

        for i in included_past_positions:
            i.append(SequenceMatcher(None, i[1], position).ratio())
            list_of_similar_positions.append(i)

    else:
        pass

    list_of_similar_positions.sort(key=operator.itemgetter(2), reverse=True)

    return list_of_similar_positions


def default_template_resume_pdf(environment, admin, password, resume, position_raw, industry, user_id):
    # Auth token for API calls

    headers = get_token(admin, password, environment)

    # API endpoints for creating tailored resume pdf components

    create_tailored_resume_personal_url = environment + "/resume/create-tailored-personal/"
    create_tailored_resume_experience_url = environment + "/resume/create-tailored-experience/"
    create_tailored_resume_education_url = environment + "/resume/create-tailored-education/"
    create_tailored_resume_reference_url = environment + "/resume/create-tailored-reference/"

    def post_resume_experience(resume_data, experience_start_date, experience_end_date):

        resume_data = {
            "resume_id": user_id,
            "company": resume_data["company_name"],
            "position": resume_data["position_name"],
            "start_date": experience_start_date,
            "end_date": experience_end_date,
            "location": "",
            "position_description": resume_data["position_description"],
            "selected_accomplishment_1": resume_data["selected_accomplishment_1"],
            "selected_accomplishment_2": resume_data["selected_accomplishment_2"],
            "selected_accomplishment_3": resume_data["selected_accomplishment_3"],
        }

        requests.post(create_tailored_resume_experience_url, headers=headers, data=resume_data)

    def post_resume_personal(resume_data):

        resume_data = {
            "resume_id": user_id,
            "first_name": resume_data["first_name"],
            "middle_name": resume_data["middle_name"],
            "last_name": resume_data["last_name"],
            "address": resume_data["address"],
            "city": resume_data["city"],
            "state": resume_data["state"],
            "country": resume_data["country"],
            "zip_code": resume_data["zip_code"],
            "phone": resume_data["phone"],
            "skills": resume_data["skills_tags"],
            "tools": resume_data["tools_tags"],
            "languages": resume_data["languages"],
        }

        requests.post(create_tailored_resume_personal_url, headers=headers, data=resume_data)

    def post_resume_education(resume_data, education_start_date, education_end_date):

        resume_data = {
            "resume_id": user_id,
            "degree": resume_data["degree"],
            "institution": resume_data["institution_name"],
            "start_date": education_start_date,
            "end_date": education_end_date,
        }

        requests.post(create_tailored_resume_education_url, headers=headers, data=resume_data)

    def post_resume_reference(resume_data):

        resume_data = {
            "resume_id": user_id,
            "first_name": resume_data["first_name"],
            "current_position": resume_data["current_position_name"],
            "phone": resume_data["phone"],
            "email": resume_data["email"],
        }

        requests.post(create_tailored_resume_reference_url, headers=headers, data=resume_data)

    # Initialize
    user_id = str(user_id)
    random_combo = gen_version_number(10)

    position = position_raw.replace(" ", "")

    full_filename = position + "_resume_user_id_" + user_id + "_" + str(random_combo) + ".pdf"

    if resume:

        if resume["first_name"] == "None":
            first_name = ""
        elif resume["first_name"]:
            first_name = resume["first_name"].title()
        else:
            first_name = ""

        if resume["middle_name"] == "None":
            middle_name = ""
        elif resume["middle_name"]:
            middle_name = resume["middle_name"].title()
        else:
            middle_name = ""

        if resume["last_name"] == "None":
            last_name = ""
        elif resume["last_name"]:
            last_name = resume["last_name"].title()
        else:
            last_name = ""

        if all(i for i in [first_name, middle_name, last_name]):
            candidate_name = ' '.join([first_name, middle_name, last_name])
        elif all(i for i in [first_name, last_name]):
            candidate_name = ' '.join([first_name, last_name])
        elif first_name:
            candidate_name = first_name
        elif last_name:
            candidate_name = last_name
        else:
            candidate_name = "No name provided - please " \
                             "add a name in the resume tab under personal"

        """ WeasyPrint formatting """

        # Initate all elements for header

        if resume["address"]:
            address_text = '<p>{}<br>'.format(resume["address"].title())

            if resume["city"]:
                address_text += '{}<br>'.format(resume["city"].title())
            else:
                pass

            if resume["state"]:
                address_text += '{}<br>'.format(resume["state"])
            else:
                pass

            if resume["zip_code"]:
                address_text += '{}<br>'.format(resume["zip_code"])
            else:
                pass
        else:
            address_text = ""

        if resume["phone"]:
            phone_text = "<li>e: {}</li>".format(resume["phone"])
        else:
            phone_text = ''

        if resume["email"]:
            email_text = "<li>e: {}</li>".format(resume["email"])
        else:
            email_text = ''

        contact_text = f'<ul>{phone_text}{email_text}</ul>'

        header_template = f"""
        <html>
            <head>
            <title>{first_name} {last_name}</title>
            <link type="text/css" rel="stylesheet" href="style.css">
            <link href='http://fonts.googleapis.com/css?family=Rokkitt:400,700|Lato:400,300' rel='stylesheet' type='text/css'>

            </head>
            <body class="page">
            <div id="cv">
                <div class="mainDetails">

                    <div id="name">
                        <h1>{first_name} {last_name}</h1>
                        <h2>{position_raw}</h2>
                        {address_text}
                    </div>

                    <div id="contactDetails">
                        {contact_text}
                    </div>
                    <div class="clear"></div>
                </div>

                <div id="mainArea">
        """

        # Initiate all elements for body

        # Profile

        profile_summmary_template = ''

        if resume["profile_summary"]:
            profile_summmary_template += f"""
                    <section>
                        <article>
                            <div class="sectionTitle">
                                <h1>Profile Summary</h1>
                            </div>

                            <div class="sectionContent">
                                <p>{resume["profile_summary"]}</p>
                            </div>
                        </article>
                        <div class="clear"></div>
                    </section>"""
        else:
            pass

        # Experience:

        experience_text = ''

        if resume["experience"]:

            order = resume_order(position_raw, industry, resume["experience"])

            if order:

                for i in order:

                    experience_text += '<article>'

                    for k in resume["experience"]:

                        if k["id"] == i[0]:

                            # Populating story list to later create the resume

                            experience_text += f'<h2>{k["company_name"]}</h2>'

                            if k["work_start_date"]:
                                start_dmy = datetime.strptime(k["work_start_date"], '%Y-%m-%d')
                                start_date = str(start_dmy.year)
                            else:
                                start_date = ""

                            if k["work_end_date"]:
                                end_dmy = datetime.strptime(k["work_end_date"], '%Y-%m-%d')
                                end_date = str(end_dmy.year)
                            else:
                                end_date = "Present"

                            position_line = k["position_name"] + ", " + start_date + " - " + end_date

                            experience_text += f'<p class="subDetails">{position_line}</p>'

                            experience_text += f'<p>{k["position_description"]}</p>'

                            experience_text_bullet_points = '<ul style="text-indent: 2em;">'

                            if k["selected_accomplishment_1"]:
                                experience_text_bullet_points += f'<li>{k["selected_accomplishment_1"]}</li>'
                                # k["selected_accomplishment_1"])
                            if k["selected_accomplishment_2"]:
                                experience_text_bullet_points += f'<li>{k["selected_accomplishment_2"]}</li>'
                                # k["selected_accomplishment_2"])
                            if k["selected_accomplishment_3"]:
                                experience_text_bullet_points += f'<li>{k["selected_accomplishment_3"]}</li>'

                            experience_text_bullet_points += '</ul>'

                            experience_text += experience_text_bullet_points

                            # Create data to post to API create endpoint

                            post_resume_experience(k, start_date, end_date)

                            experience_text += '<p></p>'

                        else:
                            pass
                    experience_text += '</article>'

            else:

                for i in resume["experience"]:

                    experience_text += '<article>'

                    # Populating story list to later create the resume

                    experience_text += f'<h2>{i["company_name"]}</h2>'

                    if i["work_start_date"]:
                        start_dmy = datetime.strptime(i["work_start_date"], '%Y-%m-%d')
                        start_date = str(start_dmy.year)
                    else:
                        start_date = ""

                    if i["work_end_date"]:
                        end_dmy = datetime.strptime(i["work_end_date"], '%Y-%m-%d')
                        end_date = str(end_dmy.year)
                    else:
                        end_date = "Present"

                    print("TEST: ", i["position_name"])

                    position_line = i["position_name"] + ", " + start_date + " - " + end_date

                    experience_text += f'<p class="subDetails">{position_line}</p>'

                    experience_text += f'<p>{i["position_description"]}</p>'

                    experience_text_bullet_points = '<ul style="text-indent: 1.2em;">'

                    if i["selected_accomplishment_1"]:
                        experience_text_bullet_points += f'<li>{i["selected_accomplishment_1"]}</li>'
                        # k["selected_accomplishment_1"])
                    if i["selected_accomplishment_2"]:
                        experience_text_bullet_points += f'<li>{i["selected_accomplishment_2"]}</li>'
                        # k["selected_accomplishment_2"])
                    if i["selected_accomplishment_3"]:
                        experience_text_bullet_points += f'<li>{i["selected_accomplishment_3"]}</li>'

                    experience_text_bullet_points += '</ul>'

                    experience_text += experience_text_bullet_points

                    # Create data to post to API create endpoint

                    post_resume_experience(i, start_date, end_date)

                    experience_text += '<p></p>'

                    experience_text += '</article>'

        else:
            pass

        work_experience_template = f"""
        <section>
        <div class="sectionTitle">
            <h1>Work Experience</h1>
        </div>
        <div class="sectionContent">
            {experience_text}
        </div>    
        <div class="sectionContent">
        </div>
        <div class="clear"></div>
        </section>
        """

        # Education

        education_text = ''

        if resume["education"]:
            for i in resume["education"]:
                education_text += '<article>'
                education_text += f'<h2>{i["institution_name"].title()}</h2>'

                degree_start_dmy = datetime.strptime(i["education_start_date"], "%Y-%m-%d")
                degree_start = str(degree_start_dmy.year)
                degree_end_dmy = datetime.strptime(i["education_end_date"], "%Y-%m-%d")
                degree_end = str(degree_end_dmy.year)

                degree_line_full = i["degree"] + ", " + degree_start + " - " + degree_end

                education_text += f'<p>{degree_line_full}</p>'

                post_resume_education(i, degree_start, degree_end)

                education_text += '</article>'

        else:
            pass

        education_template = f"""
        <section>
            <div class="sectionTitle">
                <h1>Education</h1>
            </div>
    
            <div class="sectionContent">
                {education_text}
            </div>
            <div class="clear"></div>
        </section>
        """

        # Skills

        skills_text = ''

        if resume["skills_tags"]:
            for i in resume['skills_tags']:
                skills_text += f'<li>{i}</li>'
        else:
            pass

        skills_template = f"""
        <section>
			<div class="sectionTitle">
				<h1>Skills</h1>
			</div>

			<div class="sectionContent">
				<ul class="keySkills">
					{skills_text}
				</ul>
			</div>
			<div class="clear"></div>
		</section>"""

        # Tools

        tools_text = ''

        try:

            if resume["tools_tags"]:

                for i in resume["tools_tags"]:
                    tools_text += f'<li>{i}</li>'

                tools_template = f"""
                        <section>
                			<div class="sectionTitle">
                				<h1>Tools</h1>
                			</div>

                			<div class="sectionContent">
                				<ul class="keySkills">
                					{tools_text}
                				</ul>
                			</div>
                			<div class="clear"></div>
                		</section>"""

            else:
                tools_template = ""
                pass

        except:
            tools_template = ""
            pass

        # Languages

        languages_text = ''

        if resume["languages"]:
            for language_group in resume["languages"]:
                language_sentence = language_group['language'] + ": " + language_group['level'].lower().capitalize()
                languages_text += f'<p>{language_sentence}</p>'  # '<font size=11>{}</font>'.format(language_sentence)
        else:
            pass

        languages_template = f"""
        <section>
			<div class="sectionTitle">
				<h1>Languages</h1>
			</div>

			<div class="sectionContent">
				{languages_text}
			</div>
			<div class="clear"></div>
		</section>"""

        # References

        references_text = ''

        if resume["referees"]:

            for i in resume["referees"]:

                references_text += '<article>'

                if i["first_name"] and i["last_name"]:
                    full_name = i["first_name"].capitalize() + " " + i["last_name"].capitalize()
                    references_text += f'<h2>{full_name}</h2>'
                elif i["first_name"]:
                    references_text += f'<h2>{i["first_name"]}</h2>'
                else:
                    pass

                if i["current_position_name"]:
                    references_text += f'<p class="subDetails">{i["current_position_name"]}</p>'
                else:
                    pass

                if i["phone"]:
                    references_text += f'<p>Phone: {i["phone"]}</p>'
                else:
                    pass

                if i["email"]:
                    references_text += f'<p>Email: {i["email"]}</p>'
                else:
                    pass

                post_resume_reference(i)

                references_text += '</article>'

        else:
            pass

        references_template = f"""
        <section>
			<div class="sectionTitle">
				<h1>References</h1>
			</div>

			<div class="sectionContent">
				{references_text}
			</div>
			<div class="clear"></div>
		</section>"""

        body_template = '<div id="mainArea">' + profile_summmary_template + work_experience_template + \
                        education_template + skills_template + tools_template + languages_template + \
                        references_template + '</div'

        footer_template = f"""
        </div>
        </body>
        </html>
        """

        template = header_template + body_template + footer_template

        # Generate pdf and Upload to s3 using Weasyprint and boto3 respectively

        font_config = FontConfiguration()

        html = CustomHTML(string=template)

        css = [
            CSS(filename='./jobassistant_coverletter/jobassistant_coverletter/job_application/weasyprint_css/style.css'),
        ]

        object_url = html.write_pdf_and_store_s3(
            full_filename,
            stylesheets=css,
            font_config=font_config,
            env_url=environment,
            data_type='resume'
        )
    else:
        object_url = None

    return object_url
