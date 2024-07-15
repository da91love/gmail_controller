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
                    <div>This is Grace, brand manager for Branden.</div>
                    <div>Branden is a travel essential brand that designs packing cubes to maximize space and organize for travels, making packing for efficient and stress-free. We have been looking to work with more influential TikTokers, and I suggested your channel for your successful works with other brands.</div>
                    <br/>
                    <div>You can take a look at our products here: <a href="https://www.amazon.com/stores/Branden_US/page/FB8BEEC9-1367-4EDB-A93D-000FB0A0AD0A?ref_=ast_bln">Compression Packing Cubes</a></div>
                    <br/>
                    <div>To provide you with a clearer picture, we've attached the collaboration brief here.</div>
                    <div>You may also search "#branden_global" on Tiktok to check out our previous collaborations.</div>
                    <br/>
                    <div>Click this link if you want to check out guideline details! <a href="https://drive.google.com/file/d/1U4dv2QkR4EUGdrpcZkLLW_nzZXme-ivK/view">Branden Packing cubes guideline</a> </div>
                    <br/>
                    <div>If you are interested, please suggest your desired rate for the content.</div>
                    <div>We’d love to speak about the next steps soon!</div>
                    <br/>
                    <div>Thanks and regards,, Grace</div>
                    
                    <span>&nbsp;</span>
                    <div><b>Tiktok: @branden_global</b></div>
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