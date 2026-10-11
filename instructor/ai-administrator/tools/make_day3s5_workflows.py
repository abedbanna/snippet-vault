"""Write the two importable n8n workflows for Day 3 Session 5 into workflows/.
Credentials are left empty on purpose: each instructor/participant connects their own Google account after import."""
import json, os, uuid
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'workflows')
SHEET_URL = 'PASTE-YOUR-GOOGLE-SHEET-URL-HERE'
HR_EMAIL = 'hr@example.com'

def nid(): return str(uuid.uuid4())
def node(name, typ, ver, pos, params, **extra):
    return dict(parameters=params, id=nid(), name=name, type=typ, typeVersion=ver, position=pos, **extra)
def rl_doc(): return {'__rl': True, 'mode': 'url', 'value': SHEET_URL}
def rl_sheet(n): return {'__rl': True, 'mode': 'name', 'value': n}
def append(name, pos, sheet, cols):
    return node(name, 'n8n-nodes-base.googleSheets', 4.5, pos, {
        'operation': 'append', 'documentId': rl_doc(), 'sheetName': rl_sheet(sheet),
        'columns': {'mappingMode': 'defineBelow', 'value': cols, 'matchingColumns': [], 'schema': [
            {'id': c, 'displayName': c, 'required': False, 'defaultMatch': False, 'display': True, 'type': 'string', 'canBeUsedToMatch': True} for c in cols]},
        'options': {}})
def gmail(name, pos, to, subject, body, retry=True):
    extra = {'retryOnFail': True, 'maxTries': 3, 'waitBetweenTries': 5000} if retry else {}
    return node(name, 'n8n-nodes-base.gmail', 2.1, pos, {
        'sendTo': to, 'subject': subject, 'emailType': 'text', 'message': body,
        'options': {'appendAttribution': False}}, **extra)
def cond(left, op_type, op, right=None):
    c = {'id': nid(), 'leftValue': left, 'operator': {'type': op_type, 'operation': op}}
    if right is None: c['operator']['singleValue'] = True; c['rightValue'] = ''
    else: c['rightValue'] = right
    return c
def if_node(name, pos, conds, combinator='and'):
    return node(name, 'n8n-nodes-base.if', 2.2, pos, {'conditions': {
        'options': {'caseSensitive': True, 'leftValue': '', 'typeValidation': 'loose', 'version': 2},
        'conditions': conds, 'combinator': combinator}, 'looseTypeValidation': True, 'options': {}})
def conn(*pairs):
    """pairs: (from, [[to,...] per output])"""
    return {a: {'main': [[{'node': t, 'type': 'main', 'index': 0} for t in out] for out in outs]} for a, outs in pairs}
def note(text, pos, w=360, h=180, color=7):
    return node('Note ' + nid()[:4], 'n8n-nodes-base.stickyNote', 1, pos, {'content': text, 'width': w, 'height': h, 'color': color})
def save(fn, name, nodes, connections):
    wf = {'name': name, 'nodes': nodes, 'connections': connections, 'pinData': {}, 'settings': {'executionOrder': 'v1'}, 'meta': {}}
    p = os.path.join(OUT, fn); json.dump(wf, open(p, 'w'), indent=2, ensure_ascii=False); print('wrote', p)

# ---------- 1. Leave request demo (Session 4 candidates 2 + 3: look up balance, run policy checks, decision card) ----------
FORM = 'Leave request form'
form = node(FORM, 'n8n-nodes-base.formTrigger', 2.2, [0, 0], {
    'formTitle': 'AI Caravan Ltd. - Leave request',
    'formDescription': 'Fictional company, for training only. Your manager receives a decision card.',
    'formFields': {'values': [
        {'fieldLabel': 'Full name', 'requiredField': True},
        {'fieldLabel': 'Work email', 'fieldType': 'email', 'requiredField': True},
        {'fieldLabel': 'Manager email', 'fieldType': 'email', 'requiredField': True},
        {'fieldLabel': 'Leave type', 'fieldType': 'dropdown', 'requiredField': True,
         'fieldOptions': {'values': [{'option': 'Annual leave'}, {'option': 'Unpaid leave'}]}},
        {'fieldLabel': 'First day', 'fieldType': 'date', 'requiredField': True},
        {'fieldLabel': 'Last day', 'fieldType': 'date', 'requiredField': True},
        {'fieldLabel': 'Notes for your manager', 'fieldType': 'textarea'}]},
    'responseMode': 'onReceived', 'options': {'respondWithOptions': {'values': {
        'formSubmittedText': 'Thank you. Your request was received and is being checked against the leave policy.'}}}},
    webhookId=nid())
lookup = node('Look up balance', 'n8n-nodes-base.googleSheets', 4.5, [240, 0], {
    'documentId': rl_doc(), 'sheetName': rl_sheet('Balances'),
    'filtersUI': {'values': [{'lookupColumn': 'Email', 'lookupValue': "={{ $json['Work email'] }}"}]}, 'options': {}},
    alwaysOutputData=True)
CODE = r"""// Policy HR-POL-02 (fictional): 1-2 day requests need 2 working days notice, 3+ days need 10.
// Weekend in Jordan = Friday + Saturday. Last two weeks of a quarter also need the department head.
const f = $('Leave request form').first().json;
const bal = $input.first().json || {};
const day = s => { const d = new Date(s + 'T00:00:00'); return d; };
const isWork = d => d.getDay() !== 5 && d.getDay() !== 6;
function workDays(a, b) {           // inclusive a..b
  let n = 0; const d = new Date(a);
  while (d <= b) { if (isWork(d)) n++; d.setDate(d.getDate() + 1); }
  return n;
}
const first = day(f['First day']), last = day(f['Last day']);
const today = new Date(); today.setHours(0, 0, 0, 0);
const tomorrow = new Date(today); tomorrow.setDate(today.getDate() + 1);
const dayBefore = new Date(first); dayBefore.setDate(first.getDate() - 1);
const days = last >= first ? workDays(first, last) : 0;
const notice = first > today ? workDays(tomorrow, dayBefore) : 0;
const noticeNeeded = days <= 2 ? 2 : 10;
const remaining = bal['Remaining days'] === undefined || bal['Remaining days'] === '' ? null : Number(bal['Remaining days']);
const qEnd = new Date(first.getFullYear(), Math.floor(first.getMonth() / 3) * 3 + 3, 0);
const quarterEnd = (qEnd - first) / 86400000 < 14;

const reasons = [];
if (days === 0) reasons.push('the last day is before the first day');
if (f['Leave type'] !== 'Annual leave') reasons.push('unpaid leave needs 20 days notice and the department head');
if (remaining === null) reasons.push('no balance found for ' + f['Work email']);
else if (days > remaining) reasons.push(`asks for ${days} days but only ${remaining} remain`);
if (notice < noticeNeeded) reasons.push(`${notice} working day${notice === 1 ? '' : 's'} notice, policy needs ${noticeNeeded}`);

return [{ json: {
  'Request ID': 'LR-' + Date.now().toString().slice(-6),
  'Submitted': new Date().toISOString().slice(0, 16).replace('T', ' '),
  'Employee': f['Full name'], 'Email': f['Work email'], 'Manager email': f['Manager email'],
  'Leave type': f['Leave type'], 'First day': f['First day'], 'Last day': f['Last day'],
  'Working days': days, 'Notice (working days)': notice, 'Notice needed': noticeNeeded,
  'Remaining before': remaining === null ? '' : remaining,
  'Quarter end': quarterEnd ? 'Yes' : 'No',
  'Checks pass': reasons.length === 0,
  'Reason': reasons.join('; '),
  'Status': reasons.length === 0 ? 'Pending manager' : 'Flagged for HR',
  'Notes': f['Notes for your manager'] || ''
} }];"""
checks = node('Run policy checks', 'n8n-nodes-base.code', 2, [480, 0], {'jsCode': CODE})
gate = if_node('All checks pass?', [720, 0], [cond('={{ $json["Checks pass"] }}', 'boolean', 'true')])
COLS = ['Request ID', 'Submitted', 'Employee', 'Email', 'Manager email', 'Leave type', 'First day', 'Last day',
        'Working days', 'Notice (working days)', 'Notice needed', 'Remaining before', 'Quarter end', 'Reason', 'Status']
cols = {c: '={{ $json["%s"] }}' % c for c in COLS}
log_ok = append('Log request', [960, -120], 'Requests', cols)
log_flag = append('Log flagged request', [960, 120], 'Requests', cols)
card = gmail('Decision card to manager', [1200, -120], "={{ $('Run policy checks').item.json['Manager email'] }}",
    "=Leave request {{ $('Run policy checks').item.json['Request ID'] }}: {{ $('Run policy checks').item.json['Employee'] }}, {{ $('Run policy checks').item.json['Working days'] }} days",
    """={{ $('Run policy checks').item.json['Employee'] }} asks for {{ $('Run policy checks').item.json['Leave type'].toLowerCase() }}:
{{ $('Run policy checks').item.json['First day'] }} to {{ $('Run policy checks').item.json['Last day'] }} ({{ $('Run policy checks').item.json['Working days'] }} working days).

Policy checks (automatic, all passed):
- Balance: {{ $('Run policy checks').item.json['Remaining before'] }} days remaining before this request
- Notice: {{ $('Run policy checks').item.json['Notice (working days)'] }} working days (policy needs {{ $('Run policy checks').item.json['Notice needed'] }})
{{ $('Run policy checks').item.json['Quarter end'] === 'Yes' ? '- Last two weeks of the quarter: the department head must also approve.' : '' }}
Employee note: {{ $('Run policy checks').item.json['Notes'] || 'none' }}

The decision is yours. Reply Approve or Decline within three working days.
(Training demo, AI Caravan Ltd. is fictional.)""")
to_hr = gmail('Flag to HR', [1200, 120], HR_EMAIL,
    "=Check needed: leave request {{ $('Run policy checks').item.json['Request ID'] }} ({{ $('Run policy checks').item.json['Employee'] }})",
    """=A leave request did not pass the automatic policy checks and was NOT sent to the manager.

Employee: {{ $('Run policy checks').item.json['Employee'] }} ({{ $('Run policy checks').item.json['Email'] }})
Dates: {{ $('Run policy checks').item.json['First day'] }} to {{ $('Run policy checks').item.json['Last day'] }}
Reason: {{ $('Run policy checks').item.json['Reason'] }}

Please contact the employee. (Training demo, AI Caravan Ltd. is fictional.)""")
n1 = note('## Leave request: first build\nSession 4 candidates 2 + 3: look up the balance, run the policy checks, prepare the manager\'s decision card.\n\n**Green steps only.** The manager still decides; failed checks go to HR, not to the employee.\n\nBefore testing: paste your Google Sheet URL into both Sheets nodes and connect your Google account.', [-40, -330], 520, 230, 4)
save('Day3_S5_Leave_Request_Demo.json', 'S5 Demo - Leave request',
     [form, lookup, checks, gate, log_ok, log_flag, card, to_hr, n1],
     conn((FORM, [['Look up balance']]), ('Look up balance', [['Run policy checks']]), ('Run policy checks', [['All checks pass?']]),
          ('All checks pass?', [['Log request'], ['Log flagged request']]), ('Log request', [['Decision card to manager']]),
          ('Log flagged request', [['Flag to HR']])))

# ---------- 2. Module 05 lab solution: M5 Request intake ----------
RF = 'Request form'
rform = node(RF, 'n8n-nodes-base.formTrigger', 2.2, [0, 0], {
    'formTitle': 'Request intake', 'formDescription': 'Submit a request to Operations.',
    'formFields': {'values': [
        {'fieldLabel': 'Name', 'requiredField': True},
        {'fieldLabel': 'Email', 'fieldType': 'email'},
        {'fieldLabel': 'Department', 'fieldType': 'dropdown', 'requiredField': True, 'fieldOptions': {'values': [
            {'option': 'Finance'}, {'option': 'HR'}, {'option': 'IT'}, {'option': 'Operations'}]}},
        {'fieldLabel': 'Amount', 'fieldType': 'number'},
        {'fieldLabel': 'Description', 'fieldType': 'textarea'}]},
    'responseMode': 'onReceived', 'options': {}}, webhookId=nid())
# An empty number field arrives as 0 (verified on n8n Cloud, Oct 2026), so 'not empty' is not enough: test Amount > 0.
guard = if_node('Complete?', [240, 0], [cond('={{ $json.Email }}', 'string', 'notEmpty'), cond('={{ $json.Amount }}', 'number', 'gt', 0)])
rcols = {'Timestamp': '={{ $now.toFormat("yyyy-MM-dd HH:mm") }}', 'Name': '={{ $json.Name }}', 'Email': '={{ $json.Email }}',
         'Department': '={{ $json.Department }}', 'Amount': '={{ $json.Amount }}', 'Description': '={{ $json.Description }}'}
log_new = append('Log request', [480, -100], 'Requests', {**rcols, 'Status': 'New'})
incomplete = node('Mark incomplete', 'n8n-nodes-base.set', 3.4, [480, 140], {'assignments': {'assignments': [
    {'id': nid(), 'name': 'Status', 'value': 'Incomplete', 'type': 'string'}]}, 'includeOtherFields': True, 'options': {}})
log_inc = append('Log incomplete', [720, 140], 'Requests', {**rcols, 'Status': '={{ $json.Status }}'})
big = if_node('Amount > 500?', [720, -100], [cond("={{ $('Request form').item.json.Amount }}", 'number', 'gt', 500)])
g_big = gmail('Needs approval email', [960, -200], "={{ $('Request form').item.json.Email }}", 'Request received - needs approval',
    "=Hello {{ $('Request form').item.json.Name }},\nWe have received your request for {{ $('Request form').item.json.Amount }}. Because it is above 500 it will be reviewed by a manager before processing. We will confirm within two working days.\nRegards,\nOperations")
g_small = gmail('Being processed email', [960, 0], "={{ $('Request form').item.json.Email }}", 'Request received - being processed',
    "=Hello {{ $('Request form').item.json.Name }},\nWe have received your request for {{ $('Request form').item.json.Amount }} and it is being processed.\nRegards,\nOperations")
save('Day3_S5_Request_Intake_Solution.json', 'M5 Request intake (solution)',
     [rform, guard, log_new, incomplete, log_inc, big, g_big, g_small],
     conn((RF, [['Complete?']]), ('Complete?', [['Log request'], ['Mark incomplete']]), ('Mark incomplete', [['Log incomplete']]),
          ('Log request', [['Amount > 500?']]), ('Amount > 500?', [['Needs approval email'], ['Being processed email']])))
