"""Reviewed process lessons. These are reading rules, never campaign facts."""
import hashlib

RESEARCH_LESSONS = (
    'Read every branch of AND/OR conditions; preserve all operands and strict versus inclusive thresholds.',
    'Keep activity, snapshot, registration, verification, claim and unlock dates separate.',
    'Distinguish allocated, eligible, claimed, delivered, refunded and burned amounts; a promise is not payment.',
    'Keep counts of addresses, people, profiles and projects separate; seasons do not create new issuers.',
    'Expand thousand, million and billion into full numeric units when an amount is requested; preserve the currency or token unit.',
    'Preserve bounds such as over, up to and approximately; do not replace them with exact amounts.',
    'If sources conflict or a table is unavailable, retain the uncertainty instead of choosing an unsupported value.',
    'Return only source-supported facts; historical examples are not requirements for the current campaign.',
    'Gas, deposits, token sales and rewards are different quantities; missing cost is unknown, not zero.',
    'Separate launch dates, aggregator activity windows and retirement dates. Alpha, Beta and mainnet snapshots are independent.',
    'A wallet manual is not a reward rule. Preserve conflicts between official pages and never choose an unsupported conversion rate.',
    'Do not ask for private keys or seed phrases. Key import and replay protection instructions require manual verification of official software.',
    'Turn current source-supported conditions into ordered campaign steps; do not turn historical analogies into current eligibility.',
)
LESSON_POLICY = '\n'.join(RESEARCH_LESSONS)
LESSON_VERSION = hashlib.sha256(LESSON_POLICY.encode()).hexdigest()[:16]

def typed_output_schema(expected):
    """Expose field names and types, never reference answer values."""
    names={bool:'boolean',int:'integer',float:'number',str:'string',type(None):'number_or_null'}
    return {key:names[type(value)] for key,value in expected.items()}
