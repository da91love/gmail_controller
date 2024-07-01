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
                subject = '[Paid Collaboration Opportunity with the Best Packing Organizer - Branden]'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <br/>
                    <div>This is Grace, I’m a brand manager here in Branden.</div>
                    <div>I’m reaching out to you with an exciting collaboration opportunity that I believe aligns perfectly with your TikTok channel and your audience’s interests. Our slogan, “TRAVELING BECOMES EASIER,” aligns seamlessly with your content, reflecting the authenticity and depth that resonate with you and your audience.</div>
                    <br/>
                    <div><b>Branden is currently the #1 best-selling compression packing cube in Korea! </b> </div>
                    <div>We’ve reached 400,000 in sales with 200,000 of 5stars reviews in the market, Also many Korean celebrities and mega-creators have collaborated with us</div>
                    <br/>
                    <div>For several years, we’ve extensively focused on developing compression packing cubes. </div>
                    <div>We pride ourselves with the quality of our products compared to any other competitors out in the market. With our product’s unique compression feature and your creative touch, we believe we can create even more compelling and genuine content together.</div>
                    <br/>
                    <div>If you’re interested in exploring this collaboration further, we’d love to discuss next steps at your earliest convenience.</div>
                    <div>Please let us know your thoughts and looking forward to speaking with you.</div>
                    <br/>
                    <div>Also, if you want to find out more about our product, kindly check out our Amazon storefront by searching <b>""BRANDEN PACKING CUBE""</b>!</div>
                    <br/>
                    <div>Warmest regards, Grace</div>
                    
                    <span>&nbsp;</span>
                    <div><b>Tiktok: @branden_global</b></div>
                    <div><b>Instagram: branden.seoul</b></div>
                    <div><b>Search On Amazon: Branden Compression Packing Cube</b></div>
                    
                '''
            elif seeding_num == 2:
                subject = 'Re-Collaboration offer with Branden'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <div>I'm Grace from Branden.</div>
                    <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                    <div>So I'd like to suggest a second collaboration.</div>
                    <br/>
                    <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                    <div>Warmest regards, Grace</div>
    
                    <span>&nbsp;</span>
                    <div><b>Tiktok: @branden_global</b></div>
                    <div><b>Instagram: branden.seoul</b></div>
                '''

            else:
                subject = 'Re-Collaboration offer with Eqqualberry'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <div>I'm Grace from Branden.</div>
                    <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                    <div>So I'd like to suggest a second collaboration.</div>
                    <br/>
                    <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                    <div>Warmest regards, Grace</div>
    
                    <span>&nbsp;</span>
                    <div>Tiktok: @branden_official</div>
                    <div>Instagram: branden.seoul</div>
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