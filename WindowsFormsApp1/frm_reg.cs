using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

namespace WindowsFormsApp1
{
    public partial class frm_reg : Form
    {
        public frm_reg()
        {
            InitializeComponent();
        }

        private void frm_reg_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            cn.Open();
            string q = "exec spAddClient @ТипКлиента, @ИсторияЗаказов,  @name, @last_name, @second_name," +
        "@reg_date, @login, @password, @work_place,@work_role, @passport_number";
            SqlCommand cmd_ins_cust = new SqlCommand(q, cn);
            cmd_ins_cust.Parameters.AddWithValue('@ТипКлиента', Convert.ToInt32(COMBO));
            cmd_ins_cust.Parameters.AddWithValue('');
            cmd_ins_cust.Parameters.AddWithValue('@name', TextBox1.TEXT);
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.Parameters.AddWithValue();
            cmd_ins_cust.ExecuteNonQuery();

            cn.Close();

            MessageBox.Show('Пользователь зарегистрирован!!!');
        }
    }
}
