class EmailMsgCreator:
    @staticmethod
    def get_send_mail_msg(author_unique_id, seeding_num):
        subject = None
        body = None

        if seeding_num == 1:
            subject = 'Paid Collaboration Opportunity with Eqqualberry Toner'
            body = f'''
                <div>Hi {author_unique_id},</div>
                <br/>
                <div>I trust this message finds you well. My name is Jennifer, and I represent Eqqualberry, a distinguished Korean Skincare brand that places a strong emphasis on balanced skincare, delving into the depth of quality and user comfort. Your remarkable TikTok account recently caught our eye, and we couldn't help but be captivated by your genuine passion for beauty products.</div>
                <br/>
                <div><b>Recently, we were amazed by how much attention @charinecheungg's recent TikTok video featuring our product received.</b> It's not just about the number of views; the huge amount of likes, comments, and saves clearly shows how interested TikTok viewers are in our product. Because of this, many other TikTok influencers are reaching out to us, excited about collaborating. I'm thrilled to have the opportunity to introduce our product to you in such a positive situation: <b>Eqqualberry Swimming Pool Toner- Currently ranked 14th overall for toner on Amazon.</b></div>
                <br/>
                <div>To provide you with a clearer picture, we've attached the key benefits of our product.</div>
                <br/>
                <div><b>* Key Benefits:</b></div>
                <ul>
                <li>Ideal for sensitive and reactive skin</li>
                <li>Contain Protease to gently exfoliate skin and keep pores clean</li>
                <li>Deep hydration with five berry extracts and hyaluronic acid</li>
                <li>Refines pores and reduces blackheads</li>
                <li>Fungal acne and acne safe</li>
                </ul>
                <div>We're excited about the prospect of collaborating with you on a TikTok post featuring our Swimming Pool Toner. In recognition of your creativity and influence, we're more than happy to discuss fair compensation.😉</div>
                <br/>
                <div>Let us know if this opportunity resonates with you. Looking forward to the possibility of creating something remarkable together!</div>
                <div>Please check out <b>"#eqqualberrySwimmingPoolToner"</b> in Amazon for product details😉</div>
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