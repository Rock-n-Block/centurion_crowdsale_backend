html_style='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>Ducatus Second Mail</title>
    <style type="text/css">
      body {
        margin: 0;
        padding: 0;
        min-width: 100% !important;
        font-family: sans-serif;
      }

      img {
        height: auto;
      }

      .content {
        width: 100%;
        max-width: 1000px;
      }

      .content--footer {
        width: 100%;
      }

      .header {
        text-align: center;
        padding: 20px;
      }

      .footer {
        text-align: right;
      }

      .text--center {
        text-align: center;
      }

      .text {
        font-size: 20px;
        color: #404040;
        font-weight: 300;
      }
      .code {
        color: #1737a0;
        padding-top: 5px;
      }

      .padding {
        padding-left: 30px;
        padding-right: 30px;
      }

      .text-cont {
        padding-top: 20px;
      }

      .accent {
        padding: 10px 0 0px 0;
        font-size: 25px;
        font-weight: 400;
        color: #404040;
        text-transform: uppercase;
        text-align: center;
      }

      .dear {
        font-weight: 400;
        font-size: 20px;
        color: #404040;
      }

      .body-text {
        padding: 0px 15px 15px 15px;
        font-size: 15px;
        font-weight: 300;
        text-align: center;
        line-height: 18px;
      }

      table {
        border-collapse: separate;
      }
    </style>
  </head>'''

voucher_html_body = """<body ducatus bgcolor="#ffffff">
    <table
      width="100%"
      bgcolor="#ffffff"
      border="0"
      cellpadding="0"
      cellspacing="0"
    >
      <tr>
        <td>
          <table
            bgcolor="#ffffff"
            class="content"
            align="center"
            cellpadding="0"
            cellspacing="0"
            border="0"
          >
            <tr>
              <td style="border-radius: 0px" class="header">
                <img
                  class="fix"
                  src="https://www.ducatuscoins.com/assets/img/centurion-logo.png"
                  width="370"
                  height="133"
                  border="0"
                  alt=""
                />
              </td>
            </tr>
            <tr>
              <td style="padding-bottom: 50px">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="accent">
                      Congratulations, Your lease is now active!
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding-bottom: 50px" class="padding">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="dear">Dear Partner,</td>
                  </tr>
                  <tr>
                    <td class="text text-cont">
                      Thank you for creating a Lease & Earn account on
                      centuriongm.com. We have received your payment and confirm
                      the following details:
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-cont">
                      Tokens purchased: {tokens_purchased}
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-cont">
                      Project Leased: {project_leased}
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-cont">
                      Period of Lease: {period_of_lease} months
                    </td>
                  </tr>
                  <tr>
                    <td class="text text-cont">
                      Lease Repayment: First payment will be released to your
                      account on the 4th month of your lease, it would include
                      payments from month 1 to 3.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td style="padding-bottom: 50px" class="padding">
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="text text--center">
                      Redeem your token into your Ducatus Wallet using this
                      Activation Code
                    </td>
                  </tr>
                  <tr>
                    <td class="text code text--center">{activate_code}</td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td
                style="padding-bottom: 70px; padding-top: 10px"
                class="padding"
              >
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="text">
                      You are now on your way to building generational wealth.
                      Once again, thank you for supporting our vision for a
                      thriving cashless economy and for embarking on this
                      exciting journey with us!
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
            <tr>
              <td
                style="
                  padding-bottom: 50px;
                  padding-top: 10px;
                  max-width: 205px;
                  margin-left: auto;
                  display: block;
                  padding-right: 100px;
                "
              >
                <table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td class="text">Sincerely,</td>
                  </tr>
                  <tr>
                    <td class="dear text-cont">
                      Ronny Tome, CEO The Emperor Group
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>

    <table
      bgcolor="#ffffff"
      class="content--footer"
      align="center"
      cellpadding="0"
      cellspacing="0"
      border="0"
    >
      <tr>
        <td class="footer">
          <img
            class="fix"
            src="https://www.ducatuscoins.com/assets/img/centurion-img.jpg"
            width="80%"
            border="0"
            alt=""
          />
        </td>
      </tr>
      <tr>
        <td
          style="display: block; width: 100%; height: 50px; background: #1737a0"
        ></td>
      </tr>
    </table>
  </body>
</html>
"""
