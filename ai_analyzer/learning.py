"""Small reviewed synthetic demonstrations: reading technique, never project evidence."""
import hashlib
import json

EXAMPLES = (
    {'id':'and-or', 'terms':[' or ',' and ','threshold','eligible',' або ',' или ','порог','поріг'],
     'excerpt':'Eligible users must complete 3 testnet swaps AND use the faucet, OR submit an accepted bug report.',
     'lesson':'Keep two alternatives: (3 testnet swaps AND faucet) OR accepted bug report. Do not require all three.'},
    {'id':'allocation-not-payment', 'terms':['allocation','claim','distributed','reward','нагород','винагород','вознагражд','розподіл'],
     'excerpt':'Up to 200 TEST are allocated per eligible wallet. Claims open later; no tokens have been delivered.',
     'lesson':'200 TEST is an upper allocation bound, not an actual payout. Delivered amount is not proven by allocation.'},
    {'id':'mixed-cost', 'terms':['testnet','deposit','token','faucet','тестнет','токен','кран','депозит'],
     'excerpt':'The testnet faucet is free. The separate mainnet campaign requires a deposit of 100 USDC.',
     'lesson':'Keep campaigns separate. A free faucet does not make the mainnet deposit free or suitable for test-token-only participation.'},
    {'id':'dates', 'terms':['snapshot','deadline','claim','unlock','дедлайн','розблок','разблок','снепшот'],
     'excerpt':'Snapshot: 1 May. Register by 5 May. Claim from 10 May. Tokens unlock on 1 June.',
     'lesson':'Preserve four distinct events. The registration deadline is not the claim or unlock date.'},
)

def learning_context(text, limit=2):
    lowered=' '+text.casefold()+' '
    ranked=sorted(enumerate(EXAMPLES),key=lambda pair:(-sum(term in lowered for term in pair[1]['terms']),pair[0]))
    chosen=[{k:v for k,v in row.items() if k!='terms'} for _,row in ranked
            if any(term in lowered for term in row['terms'])][:max(0,min(2,limit))]
    return {'method':'reviewed_synthetic_demonstrations_not_weight_training',
            'version':hashlib.sha256(json.dumps(EXAMPLES,sort_keys=True).encode()).hexdigest()[:16],
            'boundary':'Examples teach reading only. Never copy their values or rules into current project evidence.',
            'examples':chosen}
