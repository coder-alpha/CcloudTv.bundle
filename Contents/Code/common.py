################################################################################
TITLE = "cCloud TV | A Community based Social IPTV Service for Live TV, Movies, TV Shows & Radio"
VERSION = '0.22' # Release notation (x.y - where x is major and y is minor)
GITHUB_REPOSITORY = 'coder-alpha/CcloudTv.bundle'
PREFIX = "/video/ccloudtv"
################################################################################

USER_AGENT = 'Mozilla5.0'

GLOBAL_DISABLE_TS_TO_M3U8_SWITCH = True
GLOBAL_DISABLE_GetRedirector = True
GLOBAL_DISABLE_RTMP = False

COUNTRY_ARRAY_LIST = {'afghanistan': 'af',
 'albania': 'al',
 'algeria': 'dz',
 'american samoa': 'as',
 'andorra': 'ad',
 'angola': 'ao',
 'anguilla': 'ai',
 'antarctica': 'aq',
 'antigua and barbuda': 'ag',
 'argentina': 'ar',
 'armenia': 'am',
 'aruba': 'aw',
 'australia': 'au',
 'austria': 'at',
 'azerbaijan': 'az',
 'bahamas': 'bs',
 'bahrain': 'bh',
 'bangladesh': 'bd',
 'barbados': 'bb',
 'belarus': 'by',
 'belgium': 'be',
 'belize': 'bz',
 'benin': 'bj',
 'bermuda': 'bm',
 'bhutan': 'bt',
 'bolivia, plurinational state of': 'bo',
 'bonaire, sint eustatius and saba': 'bq',
 'bosnia and herzegovina': 'ba',
 'botswana': 'bw',
 'bouvet island': 'bv',
 'brazil': 'br',
 'british indian ocean territory': 'io',
 'brunei darussalam': 'bn',
 'bulgaria': 'bg',
 'burkina faso': 'bf',
 'burundi': 'bi',
 'cambodia': 'kh',
 'cameroon': 'cm',
 'canada': 'ca',
 'cape verde': 'cv',
 'cayman islands': 'ky',
 'central african republic': 'cf',
 'chad': 'td',
 'chile': 'cl',
 'china': 'cn',
 'christmas island': 'cx',
 'cocos (keeling) islands': 'cc',
 'colombia': 'co',
 'comoros': 'km',
 'congo': 'cg',
 'congo, the democratic republic of the': 'cd',
 'cook islands': 'ck',
 'costa rica': 'cr',
 'country name': 'code',
 'croatia': 'hr',
 'cuba': 'cu',
 'curacao': 'cw',
 'cyprus': 'cy',
 'czech republic': 'cz',
 'cote d\'ivoire': 'ci',
 'denmark': 'dk',
 'djibouti': 'dj',
 'dominica': 'dm',
 'dominican republic': 'do',
 'ecuador': 'ec',
 'egypt': 'eg',
 'el salvador': 'sv',
 'equatorial guinea': 'gq',
 'eritrea': 'er',
 'estonia': 'ee',
 'ethiopia': 'et',
 'falkland islands (malvinas)': 'fk',
 'faroe islands': 'fo',
 'fiji': 'fj',
 'finland': 'fi',
 'france': 'fr',
 'french guiana': 'gf',
 'french polynesia': 'pf',
 'french southern territories': 'tf',
 'gabon': 'ga',
 'gambia': 'gm',
 'georgia': 'ge',
 'germany': 'de',
 'ghana': 'gh',
 'gibraltar': 'gi',
 'greece': 'gr',
 'greenland': 'gl',
 'grenada': 'gd',
 'guadeloupe': 'gp',
 'guam': 'gu',
 'guatemala': 'gt',
 'guernsey': 'gg',
 'guinea': 'gn',
 'guinea-bissau': 'gw',
 'guyana': 'gy',
 'haiti': 'ht',
 'heard island and mcdonald islands': 'hm',
 'holy see (vatican city state)': 'va',
 'honduras': 'hn',
 'hong kong': 'hk',
 'hungary': 'hu',
 'iceland': 'is',
 'india': 'in',
 'indonesia': 'id',
 'iran, islamic republic of': 'ir',
 'iraq': 'iq',
 'ireland': 'ie',
 'isle of man': 'im',
 'israel': 'il',
 'italy': 'it',
 'jamaica': 'jm',
 'japan': 'jp',
 'jersey': 'je',
 'jordan': 'jo',
 'kazakhstan': 'kz',
 'kenya': 'ke',
 'kiribati': 'ki',
 'korea, democratic people\'s republic of': 'kp',
 'korea, republic of': 'kr',
 'kuwait': 'kw',
 'kyrgyzstan': 'kg',
 'lao people\'s democratic republic': 'la',
 'latvia': 'lv',
 'lebanon': 'lb',
 'lesotho': 'ls',
 'liberia': 'lr',
 'libya': 'ly',
 'liechtenstein': 'li',
 'lithuania': 'lt',
 'luxembourg': 'lu',
 'macao': 'mo',
 'macedonia, the former yugoslav republic of': 'mk',
 'madagascar': 'mg',
 'malawi': 'mw',
 'malaysia': 'my',
 'maldives': 'mv',
 'mali': 'ml',
 'malta': 'mt',
 'marshall islands': 'mh',
 'martinique': 'mq',
 'mauritania': 'mr',
 'mauritius': 'mu',
 'mayotte': 'yt',
 'mexico': 'mx',
 'micronesia, federated states of': 'fm',
 'moldova, republic of': 'md',
 'monaco': 'mc',
 'mongolia': 'mn',
 'montenegro': 'me',
 'montserrat': 'ms',
 'morocco': 'ma',
 'mozambique': 'mz',
 'myanmar': 'mm',
 'namibia': 'na',
 'nauru': 'nr',
 'nepal': 'np',
 'netherlands': 'nl',
 'new caledonia': 'nc',
 'new zealand': 'nz',
 'nicaragua': 'ni',
 'niger': 'ne',
 'nigeria': 'ng',
 'niue': 'nu',
 'norfolk island': 'nf',
 'northern mariana islands': 'mp',
 'norway': 'no',
 'oman': 'om',
 'pakistan': 'pk',
 'palau': 'pw',
 'palestine, state of': 'ps',
 'panama': 'pa',
 'papua new guinea': 'pg',
 'paraguay': 'py',
 'peru': 'pe',
 'philippines': 'ph',
 'pitcairn': 'pn',
 'poland': 'pl',
 'portugal': 'pt',
 'puerto rico': 'pr',
 'qatar': 'qa',
 'romania': 'ro',
 'russia': 'ru',
 'russian federation': 'ru',
 'rwanda': 'rw',
 'reunion': 're',
 'saint barthelemy': 'bl',
 'saint helena, ascension and tristan da cunha': 'sh',
 'saint kitts and nevis': 'kn',
 'saint lucia': 'lc',
 'saint martin (french part)': 'mf',
 'saint pierre and miquelon': 'pm',
 'saint vincent and the grenadines': 'vc',
 'samoa': 'ws',
 'san marino': 'sm',
 'sao tome and principe': 'st',
 'saudi arabia': 'sa',
 'senegal': 'sn',
 'serbia': 'rs',
 'seychelles': 'sc',
 'sierra leone': 'sl',
 'singapore': 'sg',
 'sint maarten (dutch part)': 'sx',
 'slovakia': 'sk',
 'slovenia': 'si',
 'solomon islands': 'sb',
 'somalia': 'so',
 'south africa': 'za',
 'south georgia and the south sandwich islands': 'gs',
 'south sudan': 'ss',
 'spain': 'es',
 'sri lanka': 'lk',
 'sudan': 'sd',
 'suriname': 'sr',
 'svalbard and jan mayen': 'sj',
 'swaziland': 'sz',
 'sweden': 'se',
 'switzerland': 'ch',
 'syrian arab republic': 'sy',
 'taiwan, province of china': 'tw',
 'tajikistan': 'tj',
 'tanzania, united republic of': 'tz',
 'thailand': 'th',
 'timor-leste': 'tl',
 'togo': 'tg',
 'tokelau': 'tk',
 'tonga': 'to',
 'trinidad and tobago': 'tt',
 'tunisia': 'tn',
 'turkey': 'tr',
 'turkmenistan': 'tm',
 'turks and caicos islands': 'tc',
 'tuvalu': 'tv',
 'uganda': 'ug',
 'ukraine': 'ua',
 'united arab emirates': 'ae',
 'united kingdom': 'uk',
 'england': 'uk',
 'great britain': 'uk',
 'united states': 'us',
 'united states of america': 'us',
 'united states america': 'us',
 'usa': 'us',
 'america': 'us',
 'united states minor outlying islands': 'um',
 'uruguay': 'uy',
 'uzbekistan': 'uz',
 'vanuatu': 'vu',
 'venezuela, bolivarian republic of': 've',
 'viet nam': 'vn',
 'virgin islands, british': 'vg',
 'virgin islands, u.s.': 'vi',
 'wallis and futuna': 'wf',
 'western sahara': 'eh',
 'yemen': 'ye',
 'zambia': 'zm',
 'zimbabwe': 'zw',
 'aland islands': 'ax'}
 
COUNTRY_ARRAY_LIST_SINGLETON = {'afghanistan': 'af',
 'albania': 'al',
 'algeria': 'dz',
 'american samoa': 'as',
 'andorra': 'ad',
 'angola': 'ao',
 'anguilla': 'ai',
 'antarctica': 'aq',
 'antigua and barbuda': 'ag',
 'argentina': 'ar',
 'armenia': 'am',
 'aruba': 'aw',
 'australia': 'au',
 'austria': 'at',
 'azerbaijan': 'az',
 'bahamas': 'bs',
 'bahrain': 'bh',
 'bangladesh': 'bd',
 'barbados': 'bb',
 'belarus': 'by',
 'belgium': 'be',
 'belize': 'bz',
 'benin': 'bj',
 'bermuda': 'bm',
 'bhutan': 'bt',
 'bolivia, plurinational state of': 'bo',
 'bonaire, sint eustatius and saba': 'bq',
 'bosnia and herzegovina': 'ba',
 'botswana': 'bw',
 'bouvet island': 'bv',
 'brazil': 'br',
 'british indian ocean territory': 'io',
 'brunei darussalam': 'bn',
 'bulgaria': 'bg',
 'burkina faso': 'bf',
 'burundi': 'bi',
 'cambodia': 'kh',
 'cameroon': 'cm',
 'canada': 'ca',
 'cape verde': 'cv',
 'cayman islands': 'ky',
 'central african republic': 'cf',
 'chad': 'td',
 'chile': 'cl',
 'china': 'cn',
 'christmas island': 'cx',
 'cocos (keeling) islands': 'cc',
 'colombia': 'co',
 'comoros': 'km',
 'congo': 'cg',
 'congo, the democratic republic of the': 'cd',
 'cook islands': 'ck',
 'costa rica': 'cr',
 'country name': 'code',
 'croatia': 'hr',
 'cuba': 'cu',
 'curacao': 'cw',
 'cyprus': 'cy',
 'czech republic': 'cz',
 'cote d\'ivoire': 'ci',
 'denmark': 'dk',
 'djibouti': 'dj',
 'dominica': 'dm',
 'dominican republic': 'do',
 'ecuador': 'ec',
 'egypt': 'eg',
 'el salvador': 'sv',
 'equatorial guinea': 'gq',
 'eritrea': 'er',
 'estonia': 'ee',
 'ethiopia': 'et',
 'falkland islands (malvinas)': 'fk',
 'faroe islands': 'fo',
 'fiji': 'fj',
 'finland': 'fi',
 'france': 'fr',
 'french guiana': 'gf',
 'french polynesia': 'pf',
 'french southern territories': 'tf',
 'gabon': 'ga',
 'gambia': 'gm',
 'georgia': 'ge',
 'germany': 'de',
 'ghana': 'gh',
 'gibraltar': 'gi',
 'greece': 'gr',
 'greenland': 'gl',
 'grenada': 'gd',
 'guadeloupe': 'gp',
 'guam': 'gu',
 'guatemala': 'gt',
 'guernsey': 'gg',
 'guinea': 'gn',
 'guinea-bissau': 'gw',
 'guyana': 'gy',
 'haiti': 'ht',
 'heard island and mcdonald islands': 'hm',
 'holy see (vatican city state)': 'va',
 'honduras': 'hn',
 'hong kong': 'hk',
 'hungary': 'hu',
 'iceland': 'is',
 'india': 'in',
 'indonesia': 'id',
 'iran, islamic republic of': 'ir',
 'iraq': 'iq',
 'ireland': 'ie',
 'isle of man': 'im',
 'israel': 'il',
 'italy': 'it',
 'jamaica': 'jm',
 'japan': 'jp',
 'jersey': 'je',
 'jordan': 'jo',
 'kazakhstan': 'kz',
 'kenya': 'ke',
 'kiribati': 'ki',
 'korea, democratic people\'s republic of': 'kp',
 'korea, republic of': 'kr',
 'kuwait': 'kw',
 'kyrgyzstan': 'kg',
 'lao people\'s democratic republic': 'la',
 'latvia': 'lv',
 'lebanon': 'lb',
 'lesotho': 'ls',
 'liberia': 'lr',
 'libya': 'ly',
 'liechtenstein': 'li',
 'lithuania': 'lt',
 'luxembourg': 'lu',
 'macao': 'mo',
 'macedonia, the former yugoslav republic of': 'mk',
 'madagascar': 'mg',
 'malawi': 'mw',
 'malaysia': 'my',
 'maldives': 'mv',
 'mali': 'ml',
 'malta': 'mt',
 'marshall islands': 'mh',
 'martinique': 'mq',
 'mauritania': 'mr',
 'mauritius': 'mu',
 'mayotte': 'yt',
 'mexico': 'mx',
 'micronesia, federated states of': 'fm',
 'moldova, republic of': 'md',
 'monaco': 'mc',
 'mongolia': 'mn',
 'montenegro': 'me',
 'montserrat': 'ms',
 'morocco': 'ma',
 'mozambique': 'mz',
 'myanmar': 'mm',
 'namibia': 'na',
 'nauru': 'nr',
 'nepal': 'np',
 'netherlands': 'nl',
 'new caledonia': 'nc',
 'new zealand': 'nz',
 'nicaragua': 'ni',
 'niger': 'ne',
 'nigeria': 'ng',
 'niue': 'nu',
 'norfolk island': 'nf',
 'northern mariana islands': 'mp',
 'norway': 'no',
 'oman': 'om',
 'pakistan': 'pk',
 'palau': 'pw',
 'palestine, state of': 'ps',
 'panama': 'pa',
 'papua new guinea': 'pg',
 'paraguay': 'py',
 'peru': 'pe',
 'philippines': 'ph',
 'pitcairn': 'pn',
 'poland': 'pl',
 'portugal': 'pt',
 'puerto rico': 'pr',
 'qatar': 'qa',
 'romania': 'ro',
 'russia': 'ru',
 'rwanda': 'rw',
 'reunion': 're',
 'saint barthelemy': 'bl',
 'saint helena, ascension and tristan da cunha': 'sh',
 'saint kitts and nevis': 'kn',
 'saint lucia': 'lc',
 'saint martin (french part)': 'mf',
 'saint pierre and miquelon': 'pm',
 'saint vincent and the grenadines': 'vc',
 'samoa': 'ws',
 'san marino': 'sm',
 'sao tome and principe': 'st',
 'saudi arabia': 'sa',
 'senegal': 'sn',
 'serbia': 'rs',
 'seychelles': 'sc',
 'sierra leone': 'sl',
 'singapore': 'sg',
 'sint maarten (dutch part)': 'sx',
 'slovakia': 'sk',
 'slovenia': 'si',
 'solomon islands': 'sb',
 'somalia': 'so',
 'south africa': 'za',
 'south georgia and the south sandwich islands': 'gs',
 'south sudan': 'ss',
 'spain': 'es',
 'sri lanka': 'lk',
 'sudan': 'sd',
 'suriname': 'sr',
 'svalbard and jan mayen': 'sj',
 'swaziland': 'sz',
 'sweden': 'se',
 'switzerland': 'ch',
 'syrian arab republic': 'sy',
 'taiwan, province of china': 'tw',
 'tajikistan': 'tj',
 'tanzania, united republic of': 'tz',
 'thailand': 'th',
 'timor-leste': 'tl',
 'togo': 'tg',
 'tokelau': 'tk',
 'tonga': 'to',
 'trinidad and tobago': 'tt',
 'tunisia': 'tn',
 'turkey': 'tr',
 'turkmenistan': 'tm',
 'turks and caicos islands': 'tc',
 'tuvalu': 'tv',
 'uganda': 'ug',
 'ukraine': 'ua',
 'united arab emirates': 'ae',
 'united kingdom': 'uk',
 'united states of america': 'us',
 'united states minor outlying islands': 'um',
 'uruguay': 'uy',
 'uzbekistan': 'uz',
 'vanuatu': 'vu',
 'venezuela, bolivarian republic of': 've',
 'viet nam': 'vn',
 'virgin islands, british': 'vg',
 'virgin islands, u.s.': 'vi',
 'wallis and futuna': 'wf',
 'western sahara': 'eh',
 'yemen': 'ye',
 'zambia': 'zm',
 'zimbabwe': 'zw',
 'aland islands': 'ax'}
 
COUNTRY_LIST_SINGLETON = ['AD'
					, 'AE'
					, 'AF'
					, 'AG'
					, 'AI'
					, 'AL'
					, 'AM'
					, 'AO'
					, 'AQ'
					, 'AR'
					, 'AS'
					, 'AT'
					, 'AU'
					, 'AW'
					, 'AX'
					, 'AZ'
					, 'BA'
					, 'BB'
					, 'BD'
					, 'BE'
					, 'BF'
					, 'BG'
					, 'BH'
					, 'BI'
					, 'BJ'
					, 'BL'
					, 'BM'
					, 'BN'
					, 'BO'
					, 'BQ'
					, 'BR'
					, 'BS'
					, 'BT'
					, 'BV'
					, 'BW'
					, 'BY'
					, 'BZ'
					, 'CA'
					, 'CC'
					, 'CD'
					, 'CF'
					, 'CG'
					, 'CH'
					, 'CI'
					, 'CK'
					, 'CL'
					, 'CM'
					, 'CN'
					, 'CO'
					, 'CR'
					, 'CU'
					, 'CV'
					, 'CW'
					, 'CX'
					, 'CY'
					, 'CZ'
					, 'DE'
					, 'DJ'
					, 'DK'
					, 'DM'
					, 'DO'
					, 'DZ'
					, 'EC'
					, 'EE'
					, 'EG'
					, 'EH'
					, 'ER'
					, 'ES'
					, 'ET'
					, 'FI'
					, 'FJ'
					, 'FK'
					, 'FM'
					, 'FO'
					, 'FR'
					, 'GA'
					, 'GB'
					, 'GD'
					, 'GE'
					, 'GF'
					, 'GG'
					, 'GH'
					, 'GI'
					, 'GL'
					, 'GM'
					, 'GN'
					, 'GP'
					, 'GQ'
					, 'GR'
					, 'GS'
					, 'GT'
					, 'GU'
					, 'GW'
					, 'GY'
					, 'HK'
					, 'HM'
					, 'HN'
					, 'HR'
					, 'HT'
					, 'HU'
					, 'ID'
					, 'IE'
					, 'IL'
					, 'IM'
					, 'IN'
					, 'IO'
					, 'IQ'
					, 'IR'
					, 'IS'
					, 'IT'
					, 'JE'
					, 'JM'
					, 'JO'
					, 'JP'
					, 'KE'
					, 'KG'
					, 'KH'
					, 'KI'
					, 'KM'
					, 'KN'
					, 'KP'
					, 'KR'
					, 'KW'
					, 'KY'
					, 'KZ'
					, 'LA'
					, 'LB'
					, 'LC'
					, 'LI'
					, 'LK'
					, 'LR'
					, 'LS'
					, 'LT'
					, 'LU'
					, 'LV'
					, 'LY'
					, 'MA'
					, 'MC'
					, 'MD'
					, 'ME'
					, 'MF'
					, 'MG'
					, 'MH'
					, 'MK'
					, 'ML'
					, 'MM'
					, 'MN'
					, 'MO'
					, 'MP'
					, 'MQ'
					, 'MR'
					, 'MS'
					, 'MT'
					, 'MU'
					, 'MV'
					, 'MW'
					, 'MX'
					, 'MY'
					, 'MZ'
					, 'NA'
					, 'NC'
					, 'NE'
					, 'NF'
					, 'NG'
					, 'NI'
					, 'NL'
					, 'NO'
					, 'NP'
					, 'NR'
					, 'NU'
					, 'NZ'
					, 'OM'
					, 'PA'
					, 'PE'
					, 'PF'
					, 'PG'
					, 'PH'
					, 'PK'
					, 'PL'
					, 'PM'
					, 'PN'
					, 'PR'
					, 'PS'
					, 'PT'
					, 'PW'
					, 'PY'
					, 'QA'
					, 'RE'
					, 'RO'
					, 'RS'
					, 'RU'
					, 'RW'
					, 'SA'
					, 'SB'
					, 'SC'
					, 'SD'
					, 'SE'
					, 'SG'
					, 'SH'
					, 'SI'
					, 'SJ'
					, 'SK'
					, 'SL'
					, 'SM'
					, 'SN'
					, 'SO'
					, 'SR'
					, 'SS'
					, 'ST'
					, 'SV'
					, 'SX'
					, 'SY'
					, 'SZ'
					, 'TC'
					, 'TD'
					, 'TF'
					, 'TG'
					, 'TH'
					, 'TJ'
					, 'TK'
					, 'TL'
					, 'TM'
					, 'TN'
					, 'TO'
					, 'TR'
					, 'TT'
					, 'TV'
					, 'TW'
					, 'TZ'
					, 'UA'
					, 'UG'
					, 'UK'
					, 'UM'
					, 'US'
					, 'UY'
					, 'UZ'
					, 'VA'
					, 'VC'
					, 'VE'
					, 'VG'
					, 'VI'
					, 'VN'
					, 'VU'
					, 'WF'
					, 'WS'
					, 'YE'
					, 'YT'
					, 'ZA'
					, 'ZM'
					, 'ZW'] 
 
LANGUAGES_LIST_SINGLETON = ['Akan',
'Amharic',
'Arabic',
'Assamese',
'Awadhi',
'Azerbaijani',
'Balochi',
'Belarusian',
'Bengali',
'Bhojpuri',
'Burmese',
'Cantonese',
'Chewa',
'Chhattisgarhi',
'Chittagonian',
'Croatian',
'Czech',
'Deccan',
'Dhundhari',
'Dutch',
'EasternMin',
'English',
'French',
'Fula',
'GanChinese',
'German',
'Greek',
'Gujarati',
'HaitianCreole',
'Hakka',
'Haryanvi',
'Hausa',
'Hebrew',
'Hiligaynon',
'Hindi',
'Hmong',
'Hungarian',
'Hunnanese',
'Igbo',
'Ilocano',
'Indonesian',
'Italian',
'Japanese',
'Javanese',
'Jin',
'Kannada',
'Kazakh',
'Khmer',
'Kinyarwanda',
'Kirundi',
'Konkani',
'Korean',
'Kurdish',
'Madurese',
'Magahi',
'Malagasy',
'Malayalam',
'Mandarin',
'Marathi',
'Marwari',
'Mossi',
'Nepali',
'NorthernMin',
'Oriya',
'Oromo',
'Pashto',
'Persian',
'Polish',
'Portuguese',
'Punjabi',
'Quechua',
'Romanian',
'Russian',
'Saraiki',
'Shona',
'Sindhi',
'Sinhalese',
'Somali',
'SouthernMin',
'Spanish',
'Sundanese',
'Swedish',
'Sylheti',
'Tagalog',
'Tamil',
'Telugu',
'Thai',
'Turkish',
'Turkmen',
'Ukrainian',
'Urdu',
'Uyghur',
'Uzbek',
'Vietnamese',
'Visayan',
'Wu',
'Xhosa',
'Yoruba',
'Zhuang',
'Zulu']

CATEGORIES_LIST_SINGLETON = ['Documentary','Entertainment','Family','Lifestyle','News','Movie Channels','Music','OnDemandMovies','OnDemandShows','RandomAirTime 24/7','Radio','Sports','Adult','Test']
  
def getCountryName(search_code):

	if '/' in search_code:
		str_split = search_code.split('/')
		ret_str = None
		for str in str_split:
			for country, code in COUNTRY_ARRAY_LIST_SINGLETON.iteritems():
				if code == str.lower():
					if ret_str == None:
						ret_str = country.title()
						break
					else:
						ret_str = ret_str + '/' + country.title()
						break
		if ret_str == None:
			ret_str = search_code
		return ret_str
	else:
		for country, code in COUNTRY_ARRAY_LIST_SINGLETON.iteritems():
			if code == search_code.lower():
				return country.title()
		
		return search_code
		
def getCountryCode(search_country):

	if '/' in search_country:
		str_split = search_country.split('/')
		ret_str = None
		for str in str_split:
			for country, code in COUNTRY_ARRAY_LIST_SINGLETON.iteritems():
				if country.lower() == str.lower():
					if ret_str == None:
						ret_str = code.upper()
						break
					else:
						ret_str = ret_str + '/' + code.upper()
						break
		if ret_str == None:
			ret_str = search_country
		return ret_str
	else:
		for country, code in COUNTRY_ARRAY_LIST_SINGLETON.iteritems():
			if country.lower() == search_country.lower():
				return code.upper()
		
		return search_country
		
def isCountryCodeDefined(search_code):

	for country, code in COUNTRY_ARRAY_LIST_SINGLETON.iteritems():
		if code == search_code.lower():
			return True
	
	return False
	
FILTER_WORDS = ['public-adult','adult','xxx','sex','hustler','playboy']	
	
def isFilterWord(qword):

	if ' ' in qword:
		words = qword.split(' ')
		for s_word in FILTER_WORDS:
			for word in words:
				if word.lower() in s_word.lower():
					return True
	else:
		word = qword
		for s_word in FILTER_WORDS:
				if word.lower() in s_word.lower():
					return True
	
	return False