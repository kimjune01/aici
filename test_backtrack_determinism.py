"""
Test for issue #93: pytctrl backtracking should be idempotent

This test verifies that backtracking from the same label with the same
message produces identical outputs.
"""
import pyaici.server as aici

RULE_NAME = 'C123'

prompt_pfx=f'''
You are classifying whether an incoming message matches the {RULE_NAME} rule definition below.

Given a message description of the form "message: <message content>", please print "response: Matches {RULE_NAME}" if the rule matches the message and "response: Does not match {RULE_NAME}" otherwise. On the next line, print "reason: <reason for the response>". Finally, on the next line, print "Message End".

* {RULE_NAME} rule definition:

Message is addressed at a  group (not just an individual) ("Group Targeting")

'''

messages =[
    'he deserves that',
    'he deserves that',
    'he deserves that',
]


async def main():
    await aici.FixedTokens(prompt_pfx)
    plabel = aici.Label()

    aici.set_var(f'prompt', prompt_pfx)

    # generate a response for the same message N times from the same label
    outputs = []
    for msgidx, message in enumerate(messages):
        aici.set_var(f'message_{msgidx}', message)
        await aici.FixedTokens(f'message: {message}', following=plabel)
        res = await aici.gen_text(
            stop_at='Message End', store_var=f'res_{msgidx}')
        outputs.append(res)
        
    # Verify all outputs are identical
    assert outputs[0] == outputs[1] == outputs[2], (
        f"Backtracking outputs should be deterministic.\n"
        f"Got {len(set(outputs))} distinct outputs:\n"
        f"  output[0]: {repr(outputs[0][:100])}\n"
        f"  output[1]: {repr(outputs[1][:100])}\n"
        f"  output[2]: {repr(outputs[2][:100])}"
    )
    print(f"✓ All {len(messages)} backtrack iterations produced identical output")


result = aici.start(main())
