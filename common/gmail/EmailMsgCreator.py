class EmailMsgCreator:
    @staticmethod
    def get_send_mail_msg(author_unique_id, seeding_num):
        subject = None
        body = None

        if seeding_num == 1:
            subject = '🌟Elevate Your Glow: Paid Collaboration Offer with Eqqualberry Toner💙'
            body = f'''
                <div>Hi {author_unique_id},</div>
                <br/>
                <div>I trust this message finds you in good spirits. My name is Jennifer, and I represent Eqqualberry, a distinguished Korean Skincare brand that places a strong emphasis on balanced skincare, delving into the depth of quality and user comfort. Your remarkable TikTok account recently caught our eye, and we couldn't help but be captivated by your genuine passion for beauty products. 🌈</div>
                <br/>
                <div>We're thrilled to introduce you to our standout product, the Eqqualberry Swimming Pool Toner—a skincare gem meticulously crafted with the power of Protease for delicate exfoliation and a blend of five antioxidant-rich berries paired with hyaluronic acid for deep hydration. Designed for sensitive, dry, or combination skin, the results are nothing short of radiant. ✨</div>
                <br/>
                <div><b>🍓Key Benefits:</b></div>
                <ul>
                <li>Delicate exfoliation with Protease, improving acne scars (dark spots)</li>
                <li>Deep hydration with five berry extracts and hyaluronic acid</li>
                <li>Refines pores and reduces blackheads</li>
                <li>Ideal for sensitive and dry/combination skin</li>
                </ul>
                <div>Our slogan, "Experience Radiance: For Skin Care That's Healthy and Balanced," aligns seamlessly with your beauty philosophy, reflecting the authenticity and depth that resonate with your followers.</div>
                <br/>
                <div>We're excited about the prospect of collaborating with you on a TikTok post featuring our Swimming Pool Toner. In recognition of your creativity and influence, we're more than happy to discuss fair compensation. 💖</div>
                <div>Let us know if this opportunity resonates with you. Looking forward to the possibility of creating something remarkable together!</div>
                <div>Please check out <b>"#eqqualberrySwimmingPoolToner"</b> in Amazon for product details😉</div>
                <br/>
                <div>Warmest regards, 🌷Jennifer</div>
                
                <span>&nbsp;</span>
                <div>Tiktok: @eqqualberry_us</div>
                <div>Instagram: eqqualberry_us</div>
            '''
        elif seeding_num == 2:
            subject = 'Collaboration with Eqqualberry🌟'
            body = f'''
                <div>Hi, I'm Jennifer from Eqqualberry.</div>
                <br/>
                <div>As I mentioned earlier, due to our system I start a new email thread to discuss additional contract details.</div>
                <br/>
                <div>Let's discuss next step of collaboration through this email thread!</div>
                <div>Warmest regards, 🌷Jennifer</div>

                <span>&nbsp;</span>
                <div>Tiktok: @eqqualberry_us</div>
                <div>Instagram: eqqualberry_us</div>
            '''


        return {
            'subject': subject,
            'body': body,
        }