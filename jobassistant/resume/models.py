# Model related imports
from django.db import models
from django.urls import reverse

# User model
from django.conf import settings

# Third party imports
from smart_selects.db_fields import ChainedForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from taggit_selectize.managers import TaggableManager
from taggit.models import TaggedItemBase


User = settings.AUTH_USER_MODEL


class TailoredResumePDFPersonalManager(models.Manager):

    def get_tailored_personal(self, resume_id):
        return self.filter(resume_id=resume_id)


class TailoredResumePDFPersonal(models.Model):
    objects = TailoredResumePDFPersonalManager()

    resume_id = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    tools = models.CharField(max_length=100, null=True, blank=True)
    languages = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.resume_id


class TailoredResumePDFExperienceManager(models.Manager):

    def get_tailored_experience(self, resume_id):
        return self.filter(resume_id=resume_id)


class TailoredResumePDFExperience(models.Model):
    objects = TailoredResumePDFExperienceManager()

    resume_id = models.CharField(max_length=100, null=True, blank=True)
    position= models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    position_description = models.TextField(null=True, blank=True)
    selected_accomplishment_1 = models.CharField(max_length=500, null=True, blank=True)
    selected_accomplishment_2 = models.CharField(max_length=500, null=True, blank=True)
    selected_accomplishment_3 = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.resume_id


class TailoredResumePDFEducationManager(models.Manager):

    def get_tailored_education(self, resume_id):
        return self.filter(resume_id=resume_id)


class TailoredResumePDFEducation(models.Model):
    objects = TailoredResumePDFEducationManager()

    resume_id = models.CharField(max_length=100, null=True, blank=True)
    institution = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(max_length=100, null=True, blank=True)
    end_date = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.resume_id


class TailoredResumePDFReferenceManager(models.Manager):

    def get_tailored_reference(self, resume_id):
        return self.filter(resume_id=resume_id)


class TailoredResumePDFReference(models.Model):
    objects = TailoredResumePDFReferenceManager()
    resume_id = models.CharField(max_length=100, null=True, blank=True)
    candidate = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    current_position = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.resume_id


class Positions(models.Model):
    positions = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "positions"

    def __str__(self):
        return str(self.positions)


# Reconciled positions for cover letter script
class ReconciledPositions(models.Model):
    static_positions = models.CharField(max_length=200)

    def __str__(self):
        return str(self.static_positions)


class Skill(TaggedItemBase):
    name = models.CharField(max_length=200)
    content_object = models.ForeignKey('Personal',
                                       verbose_name="skills",
                                       related_name='skills+',
                                       on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Tool(TaggedItemBase):
    name = models.CharField(max_length=200)
    content_object = models.ForeignKey('Personal',
                                       verbose_name="tools",
                                       related_name='tools+',
                                       on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


# TODO: Add complete_status to each resume component models.NullBooleanField(blank=False)


class PersonalManager(models.Manager):
    def get_personal(self, user):
        return self.filter(parent_user=user)


class Personal(models.Model):
    objects = PersonalManager()

    id = models.AutoField(primary_key=True)
    parent_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE,
                                    blank=False)
    first_name = models.CharField(max_length=50, null=True, blank=False)
    middle_name = models.CharField(max_length=50, null=True,  blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    address = models.CharField(max_length=300, null=True, blank=True)  # TODO: implement google locations in frontend
    city = models.CharField(max_length=120, null=True, blank=True)  # split address into city, state via google API etc
    state = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    phone = PhoneNumberField(blank=True, help_text="eg. +61XXXXXXXXX")  # https://github.com/stefanfoulis/django-phonenumber-field
    email = models.EmailField(max_length=250, null=True, blank=False)
    profile_summary = models.TextField(max_length=800, null=True, blank=False)
    skills = TaggableManager(verbose_name="skills",
                             related_name='skills+',
                             through=Skill,
                             blank=False)
    tools = TaggableManager(verbose_name="tools",
                            related_name='tools+',
                            through=Tool,
                             blank=False)
    complete_status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('resume:personal-update', kwargs={'pk': self.pk})

    def __str__(self):
        user = str(self.parent_user)
        return user


class IndustryCategories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = "industry categories"

    def __str__(self):
        return self.name


class SubIndustryCategories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey(IndustryCategories, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "sub-industry categories"

    def __str__(self):
        return self.name


class CompaniesManager(models.Manager):
    def create_company(self, name):
        company = self.create(companies=name)
        # do something with the book
        return company


class Companies(models.Model):
    companies = models.CharField(max_length=200)
    objects = CompaniesManager()

    def __str__(self):
        return str(self.companies)


class EducationInstitutions(models.Model):
    institutions = models.CharField(max_length=200)

    def __str__(self):
        return str(self.institutions)


class ExperienceManager(models.Manager):
    def get_experience(self, user):
        return self.filter(candidate=user)


class Experience(models.Model):
    objects = ExperienceManager()

    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    position = models.ForeignKey(Positions, on_delete=models.CASCADE, null=True, blank=False)
    company = models.CharField(max_length=100, null=True, blank=False)
    # company = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, blank=False)
    location = models.CharField(max_length=100, null=True, blank=False)
    work_start_date = models.DateField(null=True, blank=False)
    work_end_date = models.DateField(null=True, blank=True)
    currently_working_here = models.NullBooleanField(blank=False)
    industry = models.ForeignKey(IndustryCategories, on_delete=models.CASCADE, null=True, blank=False)
    subindustry = ChainedForeignKey(SubIndustryCategories,
                                    chained_field="industry",
                                    chained_model_field="parent",
                                    show_all=False,
                                    auto_choose=True,
                                    sort=True,
                                    null=True,
                                    blank=False)
    position_description = models.TextField(max_length=800, null=True, blank=True)
    selected_accomplishment_1 = models.CharField(max_length=500, null=True, blank=True)
    selected_accomplishment_2 = models.CharField(max_length=500, null=True, blank=True)
    selected_accomplishment_3 = models.CharField(max_length=500, null=True, blank=True)
    complete_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.candidate)


class EducationManager(models.Manager):
    def get_education(self, user):
        return self.filter(candidate=user)


class Education(models.Model):
    objects = EducationManager()

    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    institution = models.ForeignKey(EducationInstitutions, on_delete=models.CASCADE, null=True, blank=False)
    degree = models.CharField(max_length=100, null=True, blank=False)
    education_start_date = models.DateField(null=True, blank=False)
    education_end_date = models.DateField(null=True, blank=False)
    complete_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.candidate)


class ReferenceManager(models.Manager):
    def get_reference(self, user):
        return self.filter(candidate=user)


class Reference(models.Model):
    objects = ReferenceManager()

    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    current_position = models.ForeignKey(Positions, on_delete=models.CASCADE, null=True, blank=False)
    phone = PhoneNumberField(null=True, blank=False)  # https://github.com/stefanfoulis/django-phonenumber-field
    email = models.EmailField(max_length=250, null=True, blank=False)
    complete_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.candidate)


class LanguageManager(models.Manager):
    def get_languages(self, user):
        return self.filter(personal=user)


class Language(models.Model):
    objects = LanguageManager()

    personal = models.ForeignKey(Personal, related_name='languages', on_delete=models.CASCADE, null=True, blank=False)

    AFRIKAANS = "AFRIKAANS"
    ALBANIAN = "ALBANIAN"
    AMHARIC = "AMHARIC"
    ARABIC = "ARABIC"
    ARAMAIC = "ARAMAIC"
    ARMENIAN = "ARMENIAN"
    ASSAMESE = "ASSAMESE"
    AYMARA = "AYMARA"
    AZERBAIJANI = "AZERBAIJANI"
    BALOCHI = "BALOCHI"
    BAMANANKAN = "BAMANANKAN"
    BASHKORT = "BASHKORT"
    BASQUE = "BASQUE"
    BELARUSAN = "BELARUSAN"
    BENGALI = "BENGALI"
    BHOJPURI = "BHOJPURI"
    BISLAMA = "BISLAMA"
    BOSNIAN = "BOSNIAN"
    BRAHUI = "BRAHUI"
    BULGARIAN = "BULGARIAN"
    BURMESE = "BURMESE"
    CANTONESE = "CANTONESE"
    CATALAN = "CATALAN"
    CEBUANO = "CEBUANO"
    CHECHEN = "CHECHEN"
    CHEROKEE = "CHEROKEE"
    CROATIAN = "CROATIAN"
    CZECH = "CZECH"
    DAKOTA = "DAKOTA"
    DANISH = "DANISH"
    DARI = "DARI"
    DHOLUO = "DHOLUO"
    DUTCH = "DUTCH"
    ENGLISH = "ENGLISH"
    ESPERANTO = "ESPERANTO"
    ESTONIAN = "ESTONIAN"
    EWE = "EWE"
    FINNISH = "FINNISH"
    FRENCH = "FRENCH"
    GEORGIAN = "GEORGIAN"
    GERMAN = "GERMAN"
    GIKUYU = "GIKUYU"
    GREEK = "GREEK"
    GUARANI = "GUARANI"
    GUJARATI = "GUJARATI"
    HAITIAN = "HAITIAN"
    CREOLE = "CREOLE"
    HAUSA = "HAUSA"
    HAWAIIAN = "HAWAIIAN"
    CREOLE = "CREOLE"
    HEBREW = "HEBREW"
    HILIGAYNON = "HILIGAYNON"
    HINDI = "HINDI"
    HUNGARIAN = "HUNGARIAN"
    ICELANDIC = "ICELANDIC"
    IGBO = "IGBO"
    ILOCANO = "ILOCANO"
    INDONESIAN = "INDONESIAN"
    INUIT = "INUIT"
    IRISH = "IRISH"
    GAELIC = "GAELIC"
    ITALIAN = "ITALIAN"
    JAPANESE = "JAPANESE"
    JARAI = "JARAI"
    JAVANESE = "JAVANESE"
    KICHE = "KICHE"
    KABYLE = "KABYLE"
    KANNADA = "KANNADA"
    KASHMIRI = "KASHMIRI"
    KAZAKH = "KAZAKH"
    KHMER = "KHMER"
    KHOEKHOE = "KHOEKHOE"
    KOREAN = "KOREAN"
    KURDISH = "KURDISH"
    KYRGYZ = "KYRGYZ"
    LAO = "LAO"
    LATIN = "LATIN"
    LATVIAN = "LATVIAN"
    LINGALA = "LINGALA"
    LITHUANIAN = "LITHUANIAN"
    MACEDONIAN = "MACEDONIAN"
    MAITHILI = "MAITHILI"
    MALAGASY = "MALAGASY"
    MALAY = "MALAY"
    MALAYALAM = "MALAYALAM"
    MANDARIN = "MANDARIN"
    MARATHI = "MARATHI"
    MENDE = "MENDE"
    MONGOLIAN = "MONGOLIAN"
    NAHUATL = "NAHUATL"
    NAVAJO = "NAVAJO"
    NEPALI = "NEPALI"
    NORWEGIAN = "NORWEGIAN"
    OJIBWA = "OJIBWA"
    ORIYA = "ORIYA"
    OROMO = "OROMO"
    PASHTO = "PASHTO"
    PERSIAN = "PERSIAN"
    POLISH = "POLISH"
    PORTUGUESE = "PORTUGUESE"
    PUNJABI = "PUNJABI"
    QUECHUA = "QUECHUA"
    ROMANI = "ROMANI"
    ROMANIAN = "ROMANIAN"
    RUSSIAN = "RUSSIAN"
    RWANDA = "RWANDA"
    SAMOAN = "SAMOAN"
    SANSKRIT = "SANSKRIT"
    SERBIAN = "SERBIAN"
    SHONA = "SHONA"
    SINDHI = "SINDHI"
    SINHALA = "SINHALA"
    SLOVAK = "SLOVAK"
    SLOVENE = "SLOVENE"
    SOMALI = "SOMALI"
    SPANISH = "SPANISH"
    SWAHILI = "SWAHILI"
    SWEDISH = "SWEDISH"
    TACHELHIT = "TACHELHIT"
    TAGALOG = "TAGALOG"
    TAJIKI = "TAJIKI"
    TAMIL = "TAMIL"
    TATAR = "TATAR"
    TELUGU = "TELUGU"
    THAI = "THAI"
    TIBETIC = "TIBETIC"
    TIGRIGNA = "TIGRIGNA"
    TOK = "TOK"
    PISIN = "PISIN"
    TURKISH = "TURKISH"
    TURKMEN = "TURKMEN"
    UKRAINIAN = "UKRAINIAN"
    URDU = "URDU"
    UYGHUR = "UYGHUR"
    UZBEK = "UZBEK"
    VIETNAMESE = "VIETNAMESE"
    WARLPIRI = "WARLPIRI"
    WELSH = "WELSH"
    WOLOF = "WOLOF"
    XHOSA = "XHOSA"
    YAKUT = "YAKUT"
    YIDDISH = "YIDDISH"
    YORUBA = "YORUBA"
    YUCATEC = "YUCATEC"
    ZAPOTEC = "ZAPOTEC"
    ZULU = "ZULU"

    LANGUAGE_CHOICES = (
        (AFRIKAANS, "Afrikaans"),
        (ALBANIAN, "Albanian"),
        (AMHARIC, "Amharic"),
        (ARABIC, "Arabic"),
        (ARAMAIC, "Aramaic"),
        (ARMENIAN, "Armenian"),
        (ASSAMESE, "Assamese"),
        (AYMARA, "Aymara"),
        (AZERBAIJANI, "Azerbaijani"),
        (BALOCHI, "Balochi"),
        (BAMANANKAN, "Bamanankan"),
        (BASHKORT, "Bashkort"),
        (BASQUE, "Basque"),
        (BELARUSAN, "Belarusan"),
        (BENGALI, "Bengali"),
        (BHOJPURI, "Bhojpuri"),
        (BISLAMA, "Bislama"),
        (BOSNIAN, "Bosnian"),
        (BRAHUI, "Brahui"),
        (BULGARIAN, "Bulgarian"),
        (BURMESE, "Burmese"),
        (CANTONESE, "Cantonese"),
        (CATALAN, "Catalan"),
        (CEBUANO, "Cebuano"),
        (CHECHEN, "Chechen"),
        (CHEROKEE, "Cherokee"),
        (CROATIAN, "Croatian"),
        (CZECH, "Czech"),
        (DAKOTA, "Dakota"),
        (DANISH, "Danish"),
        (DARI, "Dari"),
        (DHOLUO, "Dholuo"),
        (DUTCH, "Dutch"),
        (ENGLISH, "English"),
        (ESPERANTO, "Esperanto"),
        (ESTONIAN, "Estonian"),
        (EWE, "Ewe"),
        (FINNISH, "Finnish"),
        (FRENCH, "French"),
        (GEORGIAN, "Georgian"),
        (GERMAN, "German"),
        (GIKUYU, "Gikuyu"),
        (GREEK, "Greek"),
        (GUARANI, "Guarani"),
        (GUJARATI, "Gujarati"),
        (HAITIAN, "Haitian"),
        (CREOLE, "Creole"),
        (HAUSA, "Hausa"),
        (HAWAIIAN, "Hawaiian"),
        (CREOLE, "Creole"),
        (HEBREW, "Hebrew"),
        (HILIGAYNON, "Hiligaynon"),
        (HINDI, "Hindi"),
        (HUNGARIAN, "Hungarian"),
        (ICELANDIC, "Icelandic"),
        (IGBO, "Igbo"),
        (ILOCANO, "Ilocano"),
        (INDONESIAN, "Indonesian"),
        (INUIT, "Inuit"),
        (IRISH, "Irish"),
        (GAELIC, "Gaelic"),
        (ITALIAN, "Italian"),
        (JAPANESE, "Japanese"),
        (JARAI, "Jarai"),
        (JAVANESE, "Javanese"),
        (KICHE, "Kiche"),
        (KABYLE, "Kabyle"),
        (KANNADA, "Kannada"),
        (KASHMIRI, "Kashmiri"),
        (KAZAKH, "Kazakh"),
        (KHMER, "Khmer"),
        (KHOEKHOE, "Khoekhoe"),
        (KOREAN, "Korean"),
        (KURDISH, "Kurdish"),
        (KYRGYZ, "Kyrgyz"),
        (LAO, "Lao"),
        (LATIN, "Latin"),
        (LATVIAN, "Latvian"),
        (LINGALA, "Lingala"),
        (LITHUANIAN, "Lithuanian"),
        (MACEDONIAN, "Macedonian"),
        (MAITHILI, "Maithili"),
        (MALAGASY, "Malagasy"),
        (MALAY, "Malay"),
        (MALAYALAM, "Malayalam"),
        (MANDARIN, "Mandarin"),
        (MARATHI, "Marathi"),
        (MENDE, "Mende"),
        (MONGOLIAN, "Mongolian"),
        (NAHUATL, "Nahuatl"),
        (NAVAJO, "Navajo"),
        (NEPALI, "Nepali"),
        (NORWEGIAN, "Norwegian"),
        (OJIBWA, "Ojibwa"),
        (ORIYA, "Oriya"),
        (OROMO, "Oromo"),
        (PASHTO, "Pashto"),
        (PERSIAN, "Persian"),
        (POLISH, "Polish"),
        (PORTUGUESE, "Portuguese"),
        (PUNJABI, "Punjabi"),
        (QUECHUA, "Quechua"),
        (ROMANI, "Romani"),
        (ROMANIAN, "Romanian"),
        (RUSSIAN, "Russian"),
        (RWANDA, "Rwanda"),
        (SAMOAN, "Samoan"),
        (SANSKRIT, "Sanskrit"),
        (SERBIAN, "Serbian"),
        (SHONA, "Shona"),
        (SINDHI, "Sindhi"),
        (SINHALA, "Sinhala"),
        (SLOVAK, "Slovak"),
        (SLOVENE, "Slovene"),
        (SOMALI, "Somali"),
        (SPANISH, "Spanish"),
        (SWAHILI, "Swahili"),
        (SWEDISH, "Swedish"),
        (TACHELHIT, "Tachelhit"),
        (TAGALOG, "Tagalog"),
        (TAJIKI, "Tajiki"),
        (TAMIL, "Tamil"),
        (TATAR, "Tatar"),
        (TELUGU, "Telugu"),
        (THAI, "Thai"),
        (TIBETIC, "Tibetic"),
        (TIGRIGNA, "Tigrigna"),
        (TOK, "Tok"),
        (PISIN, "Pisin"),
        (TURKISH, "Turkish"),
        (TURKMEN, "Turkmen"),
        (UKRAINIAN, "Ukrainian"),
        (URDU, "Urdu"),
        (UYGHUR, "Uyghur"),
        (UZBEK, "Uzbek"),
        (VIETNAMESE, "Vietnamese"),
        (WARLPIRI, "Warlpiri"),
        (WELSH, "Welsh"),
        (WOLOF, "Wolof"),
        (XHOSA, "Xhosa"),
        (YAKUT, "Yakut"),
        (YIDDISH, "Yiddish"),
        (YORUBA, "Yoruba"),
        (YUCATEC, "Yucatec"),
        (ZAPOTEC, "Zapotec"),
        (ZULU, "Zulu"),
    )

    ELEMENTARY = 'ELEMENTARY PROFICIENCY'
    LIMITED_WORKING = 'LIMITED WORKING PROFICIENCY'
    MINIMUM_PROFESSIONAL = 'MINIMUM PROFESSIONAL PROFICIENCY'
    FULL_PROFESSIONAL = 'FULL PROFESSIONAL PROFICIENCY'
    NATIVE_OR_BILINGUAL = 'NATIVE OR BILINGUAL PROFICIENCY'

    LEVEL_CHOICES = (
        (ELEMENTARY, 'Elementary Proficiency'),
        (LIMITED_WORKING, 'Limited Working Proficiency'),
        (MINIMUM_PROFESSIONAL, 'Minimum Professional Proficiency'),
        (FULL_PROFESSIONAL, 'Full Professional Proficiency'),
        (NATIVE_OR_BILINGUAL, 'Native or Bilingual Proficiency'),
    )

    language = models.CharField(
        max_length=200,
        choices=LANGUAGE_CHOICES,
        null=True
        # default="ENGLISH"
    )

    level = models.CharField(
        max_length=200,
        choices=LEVEL_CHOICES,
        null=True
        # default="ELEMENTARY PROFICIENCY"
    )

    def is_upperclass(self):
        return self.level in (
            self.ELEMENTARY,
            self.LIMITED_WORKING,
            self.MINIMUM_PROFESSIONAL,
            self.FULL_PROFESSIONAL,
            self.NATIVE_OR_BILINGUAL
        ) and self.languages in (
            self.AFRIKAANS,
            self.ALBANIAN,
            self.AMHARIC,
            self.ARABIC,
            self.ARAMAIC,
            self.ARMENIAN,
            self.ASSAMESE,
            self.AYMARA,
            self.AZERBAIJANI,
            self.BALOCHI,
            self.BAMANANKAN,
            self.BASHKORT,
            self.BASQUE,
            self.BELARUSAN,
            self.BENGALI,
            self.BHOJPURI,
            self.BISLAMA,
            self.BOSNIAN,
            self.BRAHUI,
            self.BULGARIAN,
            self.BURMESE,
            self.CANTONESE,
            self.CATALAN,
            self.CEBUANO,
            self.CHECHEN,
            self.CHEROKEE,
            self.CROATIAN,
            self.CZECH,
            self.DAKOTA,
            self.DANISH,
            self.DARI,
            self.DHOLUO,
            self.DUTCH,
            self.ENGLISH,
            self.ESPERANTO,
            self.ESTONIAN,
            self.EWE,
            self.FINNISH,
            self.FRENCH,
            self.GEORGIAN,
            self.GERMAN,
            self.GIKUYU,
            self.GREEK,
            self.GUARANI,
            self.GUJARATI,
            self.HAITIAN,
            self.CREOLE,
            self.HAUSA,
            self.HAWAIIAN,
            self.CREOLE,
            self.HEBREW,
            self.HILIGAYNON,
            self.HINDI,
            self.HUNGARIAN,
            self.ICELANDIC,
            self.IGBO,
            self.ILOCANO,
            self.INDONESIAN,
            self.INUIT,
            self.IRISH,
            self.GAELIC,
            self.ITALIAN,
            self.JAPANESE,
            self.JARAI,
            self.JAVANESE,
            self.KICHE,
            self.KABYLE,
            self.KANNADA,
            self.KASHMIRI,
            self.KAZAKH,
            self.KHMER,
            self.KHOEKHOE,
            self.KOREAN,
            self.KURDISH,
            self.KYRGYZ,
            self.LAO,
            self.LATIN,
            self.LATVIAN,
            self.LINGALA,
            self.LITHUANIAN,
            self.MACEDONIAN,
            self.MAITHILI,
            self.MALAGASY,
            self.MALAY,
            self.MALAYALAM,
            self.MANDARIN,
            self.MARATHI,
            self.MENDE,
            self.MONGOLIAN,
            self.NAHUATL,
            self.NAVAJO,
            self.NEPALI,
            self.NORWEGIAN,
            self.OJIBWA,
            self.ORIYA,
            self.OROMO,
            self.PASHTO,
            self.PERSIAN,
            self.POLISH,
            self.PORTUGUESE,
            self.PUNJABI,
            self.QUECHUA,
            self.ROMANI,
            self.ROMANIAN,
            self.RUSSIAN,
            self.RWANDA,
            self.SAMOAN,
            self.SANSKRIT,
            self.SERBIAN,
            self.SHONA,
            self.SINDHI,
            self.SINHALA,
            self.SLOVAK,
            self.SLOVENE,
            self.SOMALI,
            self.SPANISH,
            self.SWAHILI,
            self.SWEDISH,
            self.TACHELHIT,
            self.TAGALOG,
            self.TAJIKI,
            self.TAMIL,
            self.TATAR,
            self.TELUGU,
            self.THAI,
            self.TIBETIC,
            self.TIGRIGNA,
            self.TOK,
            self.PISIN,
            self.TURKISH,
            self.TURKMEN,
            self.UKRAINIAN,
            self.URDU,
            self.UYGHUR,
            self.UZBEK,
            self.VIETNAMESE,
            self.WARLPIRI,
            self.WELSH,
            self.WOLOF,
            self.XHOSA,
            self.YAKUT,
            self.YIDDISH,
            self.YORUBA,
            self.YUCATEC,
            self.ZAPOTEC,
            self.ZULU,
        )

    class Meta:
        verbose_name_plural = "languages"

    def __str__(self):
        return str(self.personal)
