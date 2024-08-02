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
                subject = '[Paid Collaboration] Emerging Kbeauty brand - Eqqualberry'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <br/>
                    <div>We are an emerging Korean skincare brand Eqqualberry.</div>
                    <div>Eqqualberry believes in a conscious and sustainable skincare for everyone. <br/>
                    <div>We have been looking to work with more influential TikTokers, and we think your audience would love to know more about us!</div>
                    <br/>
                    <div>Product : <a href="https://www.amazon.com/dp/B0CMC6S4BM?ref=cm_sw_r_cp_ud_dp_JEB7GQESK2RY26PHQ691&ref_=cm_sw_r_cp_ud_dp_JEB7GQESK2RY26PHQ691&social_share=cm_sw_r_cp_ud_dp_JEB7GQESK2RY26PHQ691&skipTwisterOG=1">Eqqualberry swimming pool toner</a></div>
                    <div>To provide you with a clearer picture, we've attached the collaboration brief <a href="https://drive.google.com/drive/u/0/folders/1Lj3mZ4QkuDCMOFzfyYpS2t0lkqWtDcFJ">here</a>.</div>
                    <div>You may also search #eqqualberry on Tiktok to check out our previous collab works.</div>
                    <br/>
                    <div>If you are interested, please suggest your desired rate for the content.</div>
                    <div>We’d love to speak about the next steps soon!</div>
                    <br/>
                    <div>Thanks and regards,</div>
                    <div>Eqqualberry</div>
                    <span>&nbsp;</span>
                    <div>Tiktok: @eqqualberry_us</div>
                    <div>Instagram: @eqqualberry_us</div>
                '''
            elif seeding_num == 2:
                subject = 'Re-Collaboration offer with Eqqualberry'
                body = f'''
                    <div>Hi {author_unique_id},</div>
                    <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                    <div>So I'd like to suggest a second collaboration.</div>
                    <br/>
                    <div>If you have an interest, Let's discuss next step of collaboration through this email thread!</div>
                    <div>Warmest regards, Eqqualberry</div>
                    <span>&nbsp;</span>
                    <div>Tiktok: @eqqualberry_us</div>
                    <div>Instagram: eqqualberry_us</div>
                '''
            else:
                subject = 'Re-Collaboration offer with Eqqualberry'
                body = f'''
                    <div>Hi, {author_unique_id},</div>
                    <div>The previous video you posted was really great! I appreciate and respect it a lot.</div>
                    <div>So I'd like to suggest a third collaboration.</div>
                    <br/>
                    <div>If you are interested, Let's discuss next step of collaboration through this email thread!</div>
                    <div>Warmest regards, Eqqualberry</div>
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
    #      <div>Warmest regards, :튤립:Jennifer</div>
    #
    #      <span>&nbsp;</span>
    #      <div>Tiktok: @eqqualberry_us</div>
    #      <div>Instagram: eqqualberry_us</div>
    #  '''