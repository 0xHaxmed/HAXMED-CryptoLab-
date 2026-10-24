"""Internationalization dictionary and language management (English LTR / Arabic RTL)."""

from typing import Dict

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import QApplication

STRINGS: Dict[str, Dict[str, str]] = {
    "en": {
        # App & Brand
        "app_title": "HAXMED CryptoLab",
        "app_subtitle": "Professional Cryptography & Cryptanalysis Toolkit",
        "brand_name": "HAXMED",
        "brand_tagline": "Advanced Cybersecurity Learning & Analysis",
        # Navigation
        "nav_dashboard": "Dashboard",
        "nav_encryption": "Encryption Studio",
        "nav_hash": "Hash Workbench",
        "nav_recovery": "Hash Recovery Lab",
        "nav_analyzer": "Cipher Analyzer",
        "nav_history": "History & Reports",
        "nav_settings": "Settings",
        "nav_about": "About CryptoLab",
        # Common Actions
        "btn_encrypt": "Encrypt",
        "btn_decrypt": "Decrypt",
        "btn_sign": "Sign",
        "btn_verify": "Verify",
        "btn_calculate": "Calculate Hash",
        "btn_compare": "Compare",
        "btn_identify": "Identify Format",
        "btn_start": "Start",
        "btn_cancel": "Cancel",
        "btn_copy": "Copy to Clipboard",
        "btn_clear": "Clear",
        "btn_export": "Export",
        "btn_import": "Import File",
        "btn_browse": "Browse...",
        "btn_generate_key": "Generate New Key",
        "btn_reset": "Reset to Defaults",
        "btn_close": "Close",
        # Dashboard
        "dash_system_status": "System & Engine Status",
        "dash_quick_actions": "Quick Workflows",
        "dash_edu_notes": "Cryptographic Highlights",
        "dash_recent_activity": "Recent Operations",
        "dash_active_tasks": "Active Background Tasks",
        "dash_no_tasks": "No background tasks currently active.",
        "dash_os_label": "Operating System",
        "dash_python_ver": "Python Runtime",
        "dash_crypto_status": "Cryptography Engine: Ready (AES-GCM, RSA-OAEP, RSA-PSS)",
        "dash_history_status": "Audit Logging",
        "dash_enabled": "Enabled",
        "dash_disabled": "Disabled (Privacy Mode)",
        # Encryption Studio
        "enc_tab_classical": "Classical Ciphers (Educational)",
        "enc_tab_modern": "Modern Cryptography (Production)",
        "enc_algo_label": "Algorithm:",
        "enc_input_label": "Input Text / Message:",
        "enc_output_label": "Output / Result:",
        "enc_key_label": "Cryptographic Key:",
        "enc_shift_label": "Shift (Integer 1-25):",
        "enc_caesar_bf_btn": "Explore All 25 Caesar Shifts",
        "enc_warning_classical": "SECURITY WARNING: Classical ciphers are educational artifacts and offer ZERO mathematical security against modern computational attacks.",
        "enc_aes_key_info": "AES-256 Key (64 Hex characters / 32 bytes):",
        "enc_aes_aad_label": "Optional Associated Data (AAD):",
        "enc_rsa_keysize_label": "Key Size (bits):",
        "enc_rsa_pubkey_label": "RSA Public Key (PEM):",
        "enc_rsa_privkey_label": "RSA Private Key (PEM):",
        "enc_rsa_size_limit": "Max plaintext for RSA-2048 OAEP is 190 bytes. For larger data, use hybrid encryption.",
        # Hash Workbench
        "hash_tab_calc": "Calculate Hash",
        "hash_tab_compare": "Compare Hashes",
        "hash_tab_identify": "Cautious Format Identification",
        "hash_tab_edu": "Hashing Education",
        "hash_input_mode": "Input Source:",
        "hash_mode_text": "Text String",
        "hash_mode_file": "File on Disk",
        "hash_file_select": "Select File to Hash:",
        "hash_digest_output": "Hexadecimal Digest:",
        "hash_compare_a": "First Digest (or Target):",
        "hash_compare_b": "Second Digest (or Computed):",
        "hash_match": "MATCH",
        "hash_no_match": "NO MATCH",
        "hash_invalid_input": "INVALID INPUT",
        "hash_identify_prompt": "Enter unknown hash or digest to inspect:",
        "hash_edu_text": (
            "• Hashing is a ONE-WAY mathematical function, NOT encryption (there is no secret key to decrypt).\n"
            "• Collision Resistance: It must be practically impossible to find two different inputs with the same hash.\n"
            "• Preimage Resistance: Given a digest, it must be impossible to reverse-engineer the original input.\n"
            "• MD5 and SHA-1 are cryptographically broken for collision resistance; do NOT use them for security.\n"
            "• Fast general hashes (SHA-256) are unsuitable for password storage; use salted, slow KDFs (Argon2id, Bcrypt)."
        ),
        # Recovery Lab
        "rec_title": "Authorized Hash Recovery Lab",
        "rec_disclaimer": "AUTHORIZED USE ONLY: This module is strictly designed for analyzing owned test vectors and authorized educational lab samples. Remote cracking or unauthorized access is strictly prohibited.",
        "rec_target_hash": "Target Hash to Verify:",
        "rec_adapter_label": "Algorithm / Adapter:",
        "rec_wordlist_label": "Local Wordlist (.txt):",
        "rec_rules_group": "Candidate Transformation Rules",
        "rec_rule_orig": "Include Original Word",
        "rec_rule_lower": "Lowercase ('word')",
        "rec_rule_upper": "Uppercase ('WORD')",
        "rec_rule_cap": "Capitalize ('Word')",
        "rec_rule_prefix": "Fixed Prefix:",
        "rec_rule_suffix": "Fixed Suffix:",
        "rec_rule_num_end": "Append Numeric Range (0 to N):",
        "rec_progress_label": "Progress & Speed:",
        "rec_status_idle": "Idle. Ready to verify candidate candidates.",
        "rec_status_running": "Evaluating candidates...",
        "rec_status_matched": "SUCCESS: Target hash candidate verified!",
        "rec_status_nomatch": "Search complete: No match identified in candidate space.",
        # Analyzer
        "ana_title": "Classical Cipher Analyzer",
        "ana_input_label": "Ciphertext to Analyze:",
        "ana_btn_analyze": "Analyze Frequency & Shifts",
        "ana_ioc_label": "Index of Coincidence (IoC):",
        "ana_ioc_explanation": "English normal IoC ≈ 0.0667. Uniform random / polyalphabetic ≈ 0.0385.",
        "ana_freq_table_header": "Letter Frequency vs. Natural English Baseline",
        "ana_caesar_rank_title": "Automated Caesar Rotation Scoring (Chi-Squared)",
        # History & Reports
        "hist_title": "Operation History & Reports",
        "hist_privacy_notice": "Privacy Protection: Plaintexts, secret keys, and passwords are NEVER saved.",
        "hist_btn_export_txt": "Export Report (TXT)",
        "hist_btn_export_json": "Export Report (JSON)",
        "hist_btn_clear": "Clear All History",
        "hist_no_records": "No operations recorded yet.",
        # Settings
        "set_title": "Application Settings",
        "set_language_label": "Interface Language:",
        "set_theme_label": "Color Theme:",
        "set_theme_dark": "Dark Charcoal (Crimson Accents)",
        "set_theme_light": "Light Modern",
        "set_privacy_group": "Privacy & Data Persistence",
        "set_enable_history": "Enable Operation History Logging (Local SQLite)",
        "set_save_btn": "Save Settings",
        # About Dialog
        "about_dialog_title": "About HAXMED CryptoLab",
        "about_text": (
            "<h3>HAXMED CryptoLab v1.0.0</h3>"
            "<p><b>Brand:</b> HAXMED Security Engineering</p>"
            "<p>A professional desktop cybersecurity learning and cryptanalysis toolkit.</p>"
            "<p>Designed with a local-first, privacy-preserving, and modular architecture.</p>"
            "<p><b>Platforms:</b> Windows and Linux</p>"
            "<p><b>License:</b> MIT License</p>"
        ),
    },
    "ar": {
        # App & Brand
        "app_title": "هاكسميد كريبتولاب",
        "app_subtitle": "منظومة التشفير وتحليل الشفرات الاحترافية",
        "brand_name": "HAXMED",
        "brand_tagline": "التعليم والتحليل السيبراني المتقدم",
        # Navigation
        "nav_dashboard": "لوحة التحكم",
        "nav_encryption": "استوديو التشفير",
        "nav_hash": "مختبر التجزئة (Hash)",
        "nav_recovery": "معمل استعادة الهاش",
        "nav_analyzer": "محلل الشفرات الكلاسيكية",
        "nav_history": "السجل والتقارير",
        "nav_settings": "الإعدادات",
        "nav_about": "حول التطبيق",
        # Common Actions
        "btn_encrypt": "تشفير",
        "btn_decrypt": "فك التشفير",
        "btn_sign": "توقيع رقمي",
        "btn_verify": "التحقق من التوقيع",
        "btn_calculate": "حساب الهاش",
        "btn_compare": "مقارنة",
        "btn_identify": "التعرف على التنسيق",
        "btn_start": "بدء",
        "btn_cancel": "إلغاء",
        "btn_copy": "نسخ إلى الحافظة",
        "btn_clear": "مسح",
        "btn_export": "تصدير",
        "btn_import": "استيراد ملف",
        "btn_browse": "استعراض...",
        "btn_generate_key": "توليد مفتاح جديد",
        "btn_reset": "استعادة الافتراضي",
        "btn_close": "إغلاق",
        # Dashboard
        "dash_system_status": "حالة النظام والمحركات",
        "dash_quick_actions": "مسارات العمل السريعة",
        "dash_edu_notes": "إضاءات تشفيرية تعليمية",
        "dash_recent_activity": "العمليات الأخيرة",
        "dash_active_tasks": "المهام النشطة في الخلفية",
        "dash_no_tasks": "لا توجد مهام نشطة حالياً في الخلفية.",
        "dash_os_label": "نظام التشغيل",
        "dash_python_ver": "بيئة بايثون",
        "dash_crypto_status": "محرك التشفير: جاهز (AES-GCM, RSA-OAEP, RSA-PSS)",
        "dash_history_status": "تسجيل سجل العمليات",
        "dash_enabled": "مفعّل",
        "dash_disabled": "معطّل (وضع الخصوصية)",
        # Encryption Studio
        "enc_tab_classical": "الشفرات الكلاسيكية (تعليمي)",
        "enc_tab_modern": "التشفير الحديث (إنتاجي)",
        "enc_algo_label": "الخوارزمية:",
        "enc_input_label": "النص المدخل / الرسالة:",
        "enc_output_label": "المخرجات / النتيجة:",
        "enc_key_label": "مفتاح التشفير:",
        "enc_shift_label": "مقدار الإزاحة (1-25):",
        "enc_caesar_bf_btn": "استعراض كافة إزاحات قيصر (25 إزاحة)",
        "enc_warning_classical": "تحذير أمني: الشفرات الكلاسيكية مخصصة للأغراض التعليمية فقط وتوفر أماناً رياضياً منعدماً ضد الهجمات الحاسوبية الحديثة.",
        "enc_aes_key_info": "مفتاح AES-256 (64 حرف ست عشري / 32 بايت):",
        "enc_aes_aad_label": "البيانات الإضافية الموثقة (AAD اختياري):",
        "enc_rsa_keysize_label": "حجم المفتاح (بت):",
        "enc_rsa_pubkey_label": "المفتاح العام RSA (PEM):",
        "enc_rsa_privkey_label": "المفتاح الخاص RSA (PEM):",
        "enc_rsa_size_limit": "أقصى حجم للنص في RSA-2048 OAEP هو 190 بايت. للبيانات الأكبر، يُستخدم التشفير الهجين.",
        # Hash Workbench
        "hash_tab_calc": "حساب الهاش",
        "hash_tab_compare": "مقارنة قيم الهاش",
        "hash_tab_identify": "التعرف الحذر على التنسيق",
        "hash_tab_edu": "مفاهيم التجزئة التعليمية",
        "hash_input_mode": "مصدر البيانات:",
        "hash_mode_text": "نص مكتوب",
        "hash_mode_file": "ملف من القرص",
        "hash_file_select": "اختر الملف لحساب الهاش:",
        "hash_digest_output": "قيمة الهاش (Hexadecimal):",
        "hash_compare_a": "الهاش الأول (أو الهدف):",
        "hash_compare_b": "الهاش الثاني (أو المحسوب):",
        "hash_match": "تطابق تام",
        "hash_no_match": "غير متطابق",
        "hash_invalid_input": "مدخلات غير صالحة",
        "hash_identify_prompt": "أدخل الهاش المراد فحصه والتعرف عليه:",
        "hash_edu_text": (
            "• دوال الهاش هي دوال رياضية باتجاه واحد، وليست تشفيراً (لا يوجد مفتاح لفك الهاش).\n"
            "• مقاومة التصادم (Collision Resistance): استحالة إيجاد مدخلين مختلفين ينتجان نفس الهاش.\n"
            "• مقاومة الصورة العكسية (Preimage Resistance): استحالة استرجاع المدخل الأصلي من قيمة الهاش.\n"
            "• خوارزميتا MD5 و SHA-1 مكسورتان أمنياً ولا يجوز استخدامهما في التطبيقات الأمنية الحديثة.\n"
            "• دوال الهاش السريعة (مثل SHA-256) لا تصلح لحفظ كلمات المرور؛ استخدم دوال بطيئة ومملحة (مثل Argon2id و Bcrypt)."
        ),
        # Recovery Lab
        "rec_title": "معمل استعادة واختبار الهاش المصرح به",
        "rec_disclaimer": "تنبيه للاستخدام المصرح به فقط: هذه الوحدة مخصصة حصرياً لاختبار العينات التعليمية والبيانات المملوكة ضمن بيئة معملية مضبوطة. يحظر تماماً أي استخدام غير مصرح به.",
        "rec_target_hash": "الهاش المستهدف للتحقق:",
        "rec_adapter_label": "الخوارزمية / المحول:",
        "rec_wordlist_label": "قائمة الكلمات المحلية (.txt):",
        "rec_rules_group": "قواعد تعديل وتوليد المرشحين",
        "rec_rule_orig": "تجربة الكلمة الأصلية",
        "rec_rule_lower": "أحرف صغيرة ('word')",
        "rec_rule_upper": "أحرف كبيرة ('WORD')",
        "rec_rule_cap": "بداية بحرف كبير ('Word')",
        "rec_rule_prefix": "بادئة ثابتة:",
        "rec_rule_suffix": "لاحقة ثابتة:",
        "rec_rule_num_end": "إضافة لاحقة أرقام (من 0 إلى N):",
        "rec_progress_label": "التقدم ومعدل السرعة:",
        "rec_status_idle": "جاهز للاختبار والتحقق من المرشحين.",
        "rec_status_running": "جارٍ التحقق من المرشحين...",
        "rec_status_matched": "نجاح: تم التحقق وتطابق المرشح مع الهاش المستهدف!",
        "rec_status_nomatch": "اكتمل البحث: لم يتم العثور على تطابق ضمن فضاء المرشحين المحدد.",
        # Analyzer
        "ana_title": "محلل الشفرات الكلاسيكية",
        "ana_input_label": "النص المشفر المراد تحليله:",
        "ana_btn_analyze": "تحليل التكرارات والإزاحات",
        "ana_ioc_label": "معامل التطابق (Index of Coincidence):",
        "ana_ioc_explanation": "القيمة المعتادة للإنجليزية ≈ 0.0667، وللتوزيع العشوائي/متعدد الأبجديات ≈ 0.0385.",
        "ana_freq_table_header": "توزيع تكرار الحروف مقارنة بالمعدل الطبيعي للغة الإنجليزية",
        "ana_caesar_rank_title": "التقييم التلقائي لإزاحات قيصر (مقياس كاي-تربيع)",
        # History & Reports
        "hist_title": "سجل العمليات والتقارير",
        "hist_privacy_notice": "حماية الخصوصية: لا يتم حفظ النصوص الأصلية أو المفاتيح السرية أو كلمات المرور نهائياً في السجل.",
        "hist_btn_export_txt": "تصدير التقرير (TXT)",
        "hist_btn_export_json": "تصدير التقرير (JSON)",
        "hist_btn_clear": "مسح كافة السجلات",
        "hist_no_records": "لا توجد عمليات مسجلة حتى الآن.",
        # Settings
        "set_title": "إعدادات التطبيق",
        "set_language_label": "لغة الواجهة:",
        "set_theme_label": "سمة الألوان:",
        "set_theme_dark": "الفحم الداكن (مع لمسات قرمزية)",
        "set_theme_light": "فاتح عصري",
        "set_privacy_group": "الخصوصية وحفظ البيانات",
        "set_enable_history": "تفعيل تسجيل سجل العمليات (SQLite محلي)",
        "set_save_btn": "حفظ الإعدادات",
        # About Dialog
        "about_dialog_title": "حول HAXMED CryptoLab",
        "about_text": (
            "<h3>هاكسميد كريبتولاب v1.0.0</h3>"
            "<p><b>العلامة التجارية:</b> HAXMED للهندسة الأمنية</p>"
            "<p>أداة مكتبية احترافية لتعلم التشفير وتحليل الشفرات والهاش للأمن السيبراني.</p>"
            "<p>مبنية وفق معايير الخصوصية الصارمة والمعالجة المحلية المستقلة.</p>"
            "<p><b>المنصات المدعومة:</b> Windows و Linux</p>"
            "<p><b>الترخيص:</b> ترخيص MIT</p>"
        ),
    },
}


class TranslationManager(QObject):
    """Manages bilingual application translations and layout direction."""

    language_changed = Signal(str)

    def __init__(self, current_lang: str = "en"):
        super().__init__()
        self._current_lang = current_lang if current_lang in STRINGS else "en"

    @property
    def current_language(self) -> str:
        return self._current_lang

    def tr(self, key: str, default: str = "") -> str:
        """Lookup translated string for current language."""
        lang_dict = STRINGS.get(self._current_lang, STRINGS["en"])
        if key in lang_dict:
            return lang_dict[key]
        return STRINGS["en"].get(key, default or key)

    def set_language(self, lang_code: str) -> None:
        """Change current interface language and update Qt layout direction."""
        if lang_code not in STRINGS:
            return
        self._current_lang = lang_code

        # Apply layout direction to the whole application
        app = QApplication.instance()
        if app:
            if lang_code == "ar":
                app.setLayoutDirection(Qt.RightToLeft)
            else:
                app.setLayoutDirection(Qt.LeftToRight)

        self.language_changed.emit(self._current_lang)


# Global singleton
i18n = TranslationManager()
