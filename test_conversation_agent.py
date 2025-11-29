"""
Standalone test file for ConversationAgent with Google Gemini
Save this as: test_conversation_agent.py
Run with: python test_conversation_agent.py
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.agents.conversation_agent import ConversationAgent
load_dotenv()
def main():
    """
    Simple test of the conversation agent
    """
    print("=" * 60)
    print("🤖 Testing AI Wardrobe Assistant with Google Gemini")
    print("=" * 60)
    print()
    
    # Step 1: Load environment variables
    print("📋 Step 1: Loading environment variables...")
    # load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found in environment")
        print("Please set environment variable: GOOGLE_API_KEY=your-key-here")
        print("Or create a .env file with: GOOGLE_API_KEY=your-key-here")
        return
    
    print(f"✅ API Key loaded: {api_key[:20]}...{api_key[-4:]}")
    print()
    
    # Step 2: Initialize Gemini
    print("📋 Step 2: Initializing Gemini...")
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini configured successfully")
    except Exception as e:
        print(f"❌ ERROR configuring Gemini: {e}")
        return
    print()
    
    # Step 3: Create conversation agent
    print("📋 Step 3: Creating conversation agent...")
    try:
        agent = ConversationAgent(
            api_key=api_key,
            model="gemini-1.5-pro"  # Use gemini-1.5-flash for faster/cheaper testing
        )
        print("✅ Conversation agent created successfully")
    except Exception as e:
        print(f"❌ ERROR creating agent: {e}")
        return
    print()
    
    # Step 4: Test with different scenarios
    print("📋 Step 4: Testing conversation scenarios...")
    print("=" * 60)
    print()
    
    # Test 1: Simple job interview question
    print("🧪 Test 1: Job Interview Question")
    print("-" * 60)
    test_message_1 = "What should I wear to a job interview?"
    print(f"You: {test_message_1}")
    print()
    
    try:
        response_1 = agent.process_message(user_message=test_message_1)
        print(f"Assistant: {response_1['response']}")
        print()
        print(f"📊 Metadata:")
        print(f"   - Intent: {response_1.get('intent', {})}")
        print(f"   - Wardrobe items: {response_1.get('wardrobe_items_count', 0)}")
        print(f"   - Recommendations: {len(response_1.get('recommendations', []))}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print()
    
    # Test 2: Weather-specific question
    print("🧪 Test 2: Weather-Specific Question")
    print("-" * 60)
    test_message_2 = "I have a date tonight at a nice restaurant. It's about 18°C and might rain. What should I wear?"
    print(f"You: {test_message_2}")
    print()
    
    try:
        response_2 = agent.process_message(user_message=test_message_2)
        print(f"Assistant: {response_2['response']}")
        print()
        print(f"📊 Metadata:")
        print(f"   - Intent: {response_2.get('intent', {})}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print()
    
    # Test 3: Follow-up question (tests conversation history)
    print("🧪 Test 3: Follow-up Question")
    print("-" * 60)
    test_message_3 = "What if I want something more casual?"
    print(f"You: {test_message_3}")
    print()
    
    try:
        # Get conversation history from previous interactions
        conversation_history = agent.get_conversation_history()
        
        response_3 = agent.process_message(
            user_message=test_message_3,
            conversation_history=conversation_history
        )
        print(f"Assistant: {response_3['response']}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print()
    
    # Test 4: With wardrobe images (mock data)
    print("🧪 Test 4: With Wardrobe Images (if available)")
    print("-" * 60)
    test_message_4 = "Based on my wardrobe, what should I wear to a wedding?"
    print(f"You: {test_message_4}")
    print()
    
    try:
        # In real usage, provide actual image paths here
        # For now, we'll test without images
        response_4 = agent.process_message(
            user_message=test_message_4,
            wardrobe_images=None  # Replace with actual image paths: ["path/to/image1.jpg", "path/to/image2.jpg"]
        )
        print(f"Assistant: {response_4['response']}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print()
    
    # Summary
    print("✅ All tests completed!")
    print()
    print("💡 Next steps:")
    print("   1. Integrate this into your FastAPI app (src/api/main.py)")
    print("   2. Add actual wardrobe image processing")
    print("   3. Test with real images from your wardrobe")
    print()
    print("📚 Gemini Tips:")
    print("   - Use 'gemini-1.5-flash' for faster/cheaper testing")
    print("   - Use 'gemini-1.5-pro' for best quality responses")
    print("   - Gemini has excellent vision capabilities for image analysis")
    print()
    print("=" * 60)


def interactive_mode():
    """
    Interactive chat mode - talk to the agent in real-time
    """
    print("=" * 60)
    print("💬 Interactive Chat Mode with Gemini")
    print("=" * 60)
    print("Type your questions and press Enter. Type 'quit' to exit.")
    print()
    
    # Initialize
    # load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GOOGLE_API_KEY not found")
        return
    
    try:
        genai.configure(api_key=api_key)
        agent = ConversationAgent(api_key=api_key, model="gemini-1.5-pro")
        print("✅ Connected to Gemini")
        print()
    except Exception as e:
        print(f"❌ ERROR initializing agent: {e}")
        return
    
    conversation_history = []
    
    while True:
        # Get user input
        try:
            user_input = input("\n💬 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 Goodbye!")
            break
        
        if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Handle special commands
        if user_input.lower() == 'reset':
            agent.reset_conversation()
            conversation_history = []
            print("\n🔄 Conversation reset!")
            continue
        
        if user_input.lower() == 'history':
            print("\n📜 Conversation History:")
            for i, msg in enumerate(conversation_history, 1):
                role = "You" if msg["role"] == "user" else "Assistant"
                print(f"{i}. {role}: {msg['content'][:100]}...")
            continue
        
        # Process message
        try:
            print("\n🤔 Thinking...")
            response = agent.process_message(
                user_message=user_input,
                conversation_history=conversation_history
            )
            
            print(f"\n🤖 Assistant: {response['response']}")
            
            # Show metadata if available
            if response.get('recommendations'):
                print(f"\n📋 {len(response['recommendations'])} outfit recommendations generated")
            
            # Update conversation history
            conversation_history = agent.get_conversation_history()
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


def quick_test():
    """
    Quick single test - fastest way to verify everything works
    """
    print("🚀 Quick Test Mode\n")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found")
        return
    
    try:
        genai.configure(api_key=api_key)
        agent = ConversationAgent(api_key=api_key, model="gemini-1.5-flash")
        
        print("Testing with Gemini Flash (fastest model)...\n")
        
        response = agent.process_message(
            user_message="What should I wear to a casual brunch?"
        )
        
        print(f"✅ Response: {response['response']}\n")
        print("🎉 System is working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive":
            # Run in interactive mode
            interactive_mode()
        elif sys.argv[1] == "quick":
            # Run quick test
            quick_test()
        else:
            print("Usage:")
            print("  python test_conversation_agent.py           # Run all tests")
            print("  python test_conversation_agent.py quick     # Quick single test")
            print("  python test_conversation_agent.py interactive # Interactive chat")
    else:
        # Run automated tests
        main()
        
        # Offer interactive mode
        print()
        response = input("Would you like to try interactive mode? (y/n): ").strip().lower()
        if response == 'y':
            print()
            interactive_mode()