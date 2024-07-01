class EmailMsgCreator:
    @staticmethod
    def get_send_mail_msg(author_unique_id, seeding_num, add_to_sys):
        subject = None
        body = None

        if add_to_sys == 1:
            subject = "[no-reply] You've been added to Eqqualberry Community!"
            body = f'''
                <div>Hi!</div>
                <br/>
                <div>You've been successfully added to Eqqualberry Creator Community.</div>
                <div>If there's a new collaboration opportunity, we will reach out to you first hand.</div>
                <div>Thank you</div>
                <br/>
                <div>Best regard</div>
                <div>Eqqualberry</div>
            '''
        else:
            if seeding_num == 1:
                subject = 'Paid Opportunity with the Best Kbeauty Brand - Eqqualberry'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <br/>
                    <div>This is Jennifer, I’m a brand manager here in Eqqualberry.</div>
                    <div>Eqqualberry is a distinguished Korean Skincare brand. We at Eqqualberry believe in a strong emphasis on balanced skincare, delving into the depth of quality and user comfort.</div>
                    <br/>
                    <div>Your TikTok channel recently caught our eye, and we couldn’t help but be captivated by your genuine passion for beauty products. Recently, we went viral and were amazed by how much attention @charinecheungg’s collaboration with us has gotten. It’s not just about the number of views; the huge amount of likes, comments, and saves clearly shows how interested TikTok viewers are in our product.</div>
                    <br/>
                    <div>Including top ranked product in Amazon "toner category", We are going to launch a renewed version of Cleanser "Daily Glow Cleanser". </div>
                    <br/>
                    <div>To provide you with a clearer picture, we've attached the key benefits of our brand and product😉</div>
                    <br/>
                    <div><b>* Key Benefits:</b></div>
                    <ul>
                    <li>Ideal for sensitive and reactive skin</li>
                    <li>Minimal and only use natural derived ingredients</li>
                    <li>All EWG green level ingredients</li>
                    </ul>
                    <div>Please check out <b>"#eqqualberry"</b> in Amazon for product details.</div>
                    <br/>
                    <div>We truly looking forward to potentially collaborating with you, and if you are interested we’d love to speak next steps soon!</div>
                    <br/>
                    <div>Warmest regards, Jennifer</div>
                    
                    <span>&nbsp;</span>
                    <div>Tiktok: @eqqualberry_us</div>
                    <div>Instagram: eqqualberry_us</div>
                '''
            elif seeding_num == 2:
                subject = 'Re-Collaboration offer with Eqqualberry'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <div>I'm Jennifer from Eqqualberry.</div>
                    <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                    <div>So I'd like to suggest a second collaboration.</div>
                    <br/>
                    <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                    <div>Warmest regards, Jennifer</div>
    
                    <span>&nbsp;</span>
                    <div>Tiktok: @eqqualberry_us</div>
                    <div>Instagram: eqqualberry_us</div>
                '''

            else:
                subject = 'Re-Collaboration offer with Eqqualberry'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <div>I'm Jennifer from Eqqualberry.</div>
                    <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                    <div>So I'd like to suggest a third collaboration.</div>
                    <br/>
                    <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                    <div>Warmest regards, Jennifer</div>
    
                    <span>&nbsp;</span>
                    <div>Tiktok: @eqqualberry_us</div>
                    <div>Instagram: eqqualberry_us</div>
                '''

        return {
            'subject': subject,
            'body': body,
        }


    # body = f'''
    #      <div>Hi {author_unique_id},</div>
    #      <div>I'm Jennifer from Eqqualberry.</div>
    #      <br/>
    #      <div>As I mentioned earlier, due to our system I start a new email thread to discuss additional contract details.</div>
    #      <br/>
    #      <div>Let's discuss next step of collaboration through this email thread!</div>
    #      <div>Warmest regards, 🌷Jennifer</div>
    #
    #      <span>&nbsp;</span>
    #      <div>Tiktok: @eqqualberry_us</div>
    #      <div>Instagram: eqqualberry_us</div>
    #  '''