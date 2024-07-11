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
                    <div>Eqqualberry is an emerging Korean Skincare brand for sensitive and reactive skin types. We believe in a conscious skincare with inclusivity and sustainability.</div>
                    <div>We are happy to suggest a collaboration opportunity for your Tiktok account. <br/>
                    <div>We currently have two main products 1) <a href="https://www.amazon.com/EQQUALBERRY-Swimming-Protease-Facial-Toner/dp/B0CMC6S4BM/ref=sr_1_1?dib=eyJ2IjoiMSJ9.Ph9WIfj2PPKubaRh0awqmZfsJMqEUL8FXHA5xpxl8YTFfKRj5bS-tOvzcz7MmpY6qL9KsArFMH0BNGEFdBWVI0U0qSHyPR2cvQFl3ioXrkc.I4E5CuXRPTh3YG7qyvFUXwUmAk9LCIpCioKgFO-F4ZM&dib_tag=se&keywords=eqqualberry&qid=1719887953&s=beauty&sr=1-1">Eqqualberry swimming pool toner<a/> which already went viral on Tiktok, and a newly launched 2) <a href="https://www.amazon.com/EQQUALBERRY-Balanced-Cleanser-Moisturizing-Cleaning/dp/B0D4996H1D/ref=sr_1_6?dib=eyJ2IjoiMSJ9.Ph9WIfj2PPKubaRh0awqmZfsJMqEUL8FXHA5xpxl8YTFfKRj5bS-tOvzcz7MmpY6qL9KsArFMH0BNGEFdBWVI0U0qSHyPR2cvQFl3ioXrkc.I4E5CuXRPTh3YG7qyvFUXwUmAk9LCIpCioKgFO-F4ZM&dib_tag=se&keywords=eqqualberry&qid=1719887910&s=beauty&sr=1-6">Eqqualberry daily glow cleanser</a>. </div>
                    <br/>
                    <div>To provide you with a clearer picture, we've attached the content guidelines for the two products😉</div>
                    <div>You may also search <b> "#eqqualberry"</b> on Tiktok to check out our previous collab works.</div>
                    <div>Clink this link if you want to check out guideline details!: <a href="https://drive.google.com/file/d/1S-3wd675AGQyPq1XaZCcTehxClgU_fSe/view?usp=drive_link">toner guideline</a>, <a href="https://drive.google.com/file/d/1FKwZPNkVFeTJnY-kq6ucUaAOQPyTMyfz/view?usp=drive_link">cleanser guideline</a>.
                    <br/>
                    <div>If you are interested, please suggest your desired rate for the content. We’d love to speak about the next steps soon!</div>
                    <br/>
                    <div>Thanks and regards, Eqqualberry</div>
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