from enum import Enum


class SystemPlaceholderPatchPath(Enum):
    """
    The first segment is the key of the system placeholder, and `/isEnabled` is the only property
    it accepts.
    """

    WRAPPED_AMPERSAND = "/wrappedAmpersand/isEnabled"
    APPLE_STRINGSDICT_PLURAL = "/appleStringsdictPlural/isEnabled"
    DOLLAR_INSIDE_BRACES = "/dollarInsideBraces/isEnabled"
    DOLLAR_OUTSIDE_BRACES = "/dollarOutsideBraces/isEnabled"
    WRAPPED_COLON = "/wrappedColon/isEnabled"
    WRAPPED_DOLLAR = "/wrappedDollar/isEnabled"
    DOLLAR_PARENTHESES = "/dollarParentheses/isEnabled"
    I18NEXT_NESTING = "/i18nextNesting/isEnabled"
    I18NEXT_LEGACY = "/i18nextLegacy/isEnabled"
    RUBY_INTERPOLATION = "/rubyInterpolation/isEnabled"
    MAILCHIMP_MERGE_TAG = "/mailchimpMergeTag/isEnabled"
    SWIFT_INTERPOLATION = "/swiftInterpolation/isEnabled"
    BRACES_TRIPLE = "/bracesTriple/isEnabled"
    BRACES_DOUBLE = "/bracesDouble/isEnabled"
    BRACES_SINGLE = "/bracesSingle/isEnabled"
    BRACES_DOUBLE_FORMATTED = "/bracesDoubleFormatted/isEnabled"
    DATE_TIME_PATTERN = "/dateTimePattern/isEnabled"
    APPLE_STRING_CATALOG_NAMED = "/appleStringCatalogNamed/isEnabled"
    PRINTF_SPECIFIER = "/printfSpecifier/isEnabled"
    PYTHON_PERCENT_FORMAT = "/pythonPercentFormat/isEnabled"
    RAILS_I18N = "/railsI18n/isEnabled"
    JAVA_MESSAGE_FORMAT = "/javaMessageFormat/isEnabled"
    DOT_NET_COMPOSITE_FORMAT = "/dotNetCompositeFormat/isEnabled"
    TWIG = "/twig/isEnabled"
    PHP_INTERPOLATION = "/phpInterpolation/isEnabled"
    FREEMARKER_DIRECTIVE = "/freemarkerDirective/isEnabled"
    WRAPPED_PERCENT = "/wrappedPercent/isEnabled"
    DATE_TIME_SPECIFIER = "/dateTimeSpecifier/isEnabled"
