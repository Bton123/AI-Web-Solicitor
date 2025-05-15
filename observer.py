def start_message_listener(driver):
    script = """
    (function() {
        const container = document.querySelector('div#message_container');
        if (!container) {
            console.warn("⚠️ Message container not found.");
            return;
        }

        // Capture initial messages to ignore them later
        const initialMessages = new Set();
        const messageElements = container.querySelectorAll('.incoming_msg, .outgoing_msg, .message, .chat-bubble, [data-message-id], [role="log"] > div');

        messageElements.forEach(msgEl => {
            const text = msgEl.innerText.trim();
            if (text) {
                initialMessages.add(text);
            }
        });

        if (window._chatObserver) {
            window._chatObserver.disconnect();
        }

        window._chatObserver = new MutationObserver((mutations) => {
            for (const mutation of mutations) {
                for (const node of mutation.addedNodes) {
                    if (node.nodeType === 1) {
                        const text = node.innerText?.trim();
                        if (text && !initialMessages.has(text)) {
                            console.log("📩 NEW MESSAGE:", text);
                            initialMessages.add(text);
                            window._lastReceivedMessage = text;
                        }
                    }
                }
            }
        });

        window._chatObserver.observe(container, {
            childList: true,
            subtree: true
        });

        console.log("✅ Message listener initialized (ignoring prior messages).");
    })();
    """
    driver.execute_script(script)
