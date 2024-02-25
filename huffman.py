from Heap import Heap, Node
import os

class HuffmanCoding:
    def __init__(self):
        self.heap = 0
        self.codes = [None] * 256
        self.frequency  = [0] * 256
        self.stack=[]
        self.reverse_mapping = {}
        self.buffer_size = 8
        self.hsize=0
        self.header=""

    def make_frequency(self ,  text):        
        for character in text: # time is n : number of char
            if(self.frequency[ord(character)] == 0): # incress the size of heap , if freq of this char 0 that mean is first time 
                self.hsize+=1
            self.frequency[ord(character)] += 1 # incress the frequency of this char
    def make_heap(self): 
        self.heap = Heap(self.hsize) # create the heap with the size we make in freq
        for i in range(0,256):
            if self.frequency[i] !=0 :#if frequency[i] == 0 ; that mean this char not used
                node = Node(chr(i), self.frequency[i]) #make new node with frequency[i] , and convert i to his char
                self.heap.insert(node) #insert the node to heap
    def make_tree(self):
        while(self.heap.get_size()>1): #check if there at least 2 elment in heap / time : n size of heap 
            node1 = self.heap.remove()
            node2 = self.heap.remove()
            merged = Node(None, (node1.freq + node2.freq)) #make new Node with nodes we removed
            merged.left = node1
            merged.right = node2
            self.heap.insert(merged) #insert the new Node
     
    def make_header(self,root , code):
        if root == None : #if the node none dont return anythins / 
            return
        if root.left == None and root.right == None : #if the root is leaf
            code+="0"+root.char
        else: #if not leaf call the make_header to left and right
            code = self.make_header(root.left,code)
            code = self.make_header(root.right,code)
            code+="1"

        return code        
   
    def make_codes(self, root, current_code):
        if(root == None):
            return

        if(root.char != None): #if the root is leaf 
            self.codes[ord(root.char)] = (root.char, current_code,len(current_code) ,  self.frequency[ord(root.char)])
            return
        #if not leaf call make_codes to left and right
        self.make_codes(root.left, current_code + "1")
        self.make_codes(root.right, current_code + "0")

    def get_encoded_text(self , text): #time n : encoded_textnumber of character in text
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[ord(character)][1] #add the code for all bytes to encoded_text
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8 # claclute the number of bits we should added as extra_padding
        for i in range(extra_padding): #time is the number of extra_padding its constant number
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding) #add the number of extra_padding to can know when decompres
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        #time is n : length of padded_encoded_text / 8 
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8): #make a loop and put every 8 bits in byte array
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, path):      
        filename, file_extension = os.path.splitext(path) # get the file name and his extention
        output_path = filename + ".huf"# declare the name and  extention of output file
        with open(path, 'rb') as file, open(output_path, 'wb') as output: #open the input , ouput file as byte
            text = ""
            while True: #time is size of file / buffer_size
                data = file.read(self.buffer_size)   #read  a group of byte and added to var text
                if not data:
                    break
                text += data.decode('latin-1')
            self.make_frequency(text)  #call the make_frequency function and give it the text and make frequency array
            self.make_heap() #make a heap from frequency array 
            self.make_tree() #make huffman tree from heap
            root = self.heap.remove()
            self.header = self.make_header(root , "") #make the header we wnat to print it in the huff file
            file_extension+="*"
            self.make_codes(root , "") #genrate the huffman table
            tr = self.get_encoded_text(text) # Replace the bytes with hir codes
            padded_encoded_text = self.pad_encoded_text(tr)  #Some time the encoded_text not fully bytes  so we add padding
            bytearr =self.get_byte_array(padded_encoded_text) #turn the final encoded_text to array of bytes
            size = len(self.header) #the length of header
            output.write((size.to_bytes(2, byteorder='big'))) # 1'st thing write the size of herder
            output.write((file_extension.encode('utf-8'))) #2'nd write the file_extension
            for i in range(0, len(self.header), self.buffer_size): #3'rd write the header as buffer / time is length of header/ 8
                buffer = self.header[i:i+self.buffer_size]
                output.write(buffer.encode('latin-1')) 
            for i in range(0, len(bytearr), self.buffer_size): #Final thing write the encoded_text as buffer / time is length of byte array/ 8
                buffer = bytearr[i:i+self.buffer_size]
                output.write(buffer) 

    def make_codes_De(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):#if the root is leaf his code be current_code
            self.reverse_mapping[current_code] = ord(root.char)
            return

        self.make_codes_De(root.left, current_code + "0") #if not leaf make_codes_De for leaft and right
        self.make_codes_De(root.right, current_code + "1")


    def remove_padding(self,  padded_encoded_text):
        padded_info = padded_encoded_text[:8]#the first byte of data is the number of padding
        extra_padding = int(padded_info, 2)#convert it to int
        padded_encoded_text = padded_encoded_text[8:] #remove the byte of padded_info
        encoded_text = padded_encoded_text[:-1*extra_padding] #remove (extra_padding) elements
        return encoded_text

    def decode_text(self , encoded_text):
        current_code = ""
        decoded_text = bytearray()
        for bit in encoded_text: 
            current_code += bit
            if(current_code in self.reverse_mapping):#search if current_code is code for any char if not add other bit
                character = self.reverse_mapping[current_code]
                decoded_text +=bytes([int(character)])
                current_code = ""

        return decoded_text

    def decompress(self , path):
        filename, file_extension = os.path.splitext(path) #get the name of file
        with open(path, 'rb') as file:
            size = bytearray()
            # Read the first 2 byte this is size of header
            byte = file.read(2)
            size=byte
            ex = bytearray()
            byte = file.read(1) 
            # Loop until reach * this is beginner of header
            while byte and byte != b'*':
                # Append the byte to the ex
                ex += byte

                # Read the next byte
                byte = file.read(1)      
            
            si = int.from_bytes(size, byteorder='big')#
            i =0 
            byte = file.read(1)      
            data=byte.decode('latin-1')
            while (i !=si-1 ):#Read the header
                byte = file.read(1) 
                z = byte.decode('latin-1')
                data+=z
                i+=1  
            for i in range(0, len(data)):#make the tree by use stack
                dat = data[i]
                if(data[i-1] == "1" and data[i-2]!="1"):
                    continue
                if(dat == "1" ):
                    self.stack.append(Node(data[i+1] , 0))
                if(dat =="0"):
                    if len(self.stack) >1 :
                        n1 = self.stack.pop()
                        n2 = self.stack.pop()
                        newN = Node(None,0) #create new node with elements we remove 
                        newN.left = n2
                        newN.right = n1
                        self.stack.append(newN)          
            self.make_codes_De(self.stack.pop() , "") #make the huffman table
            with open(filename+(ex.decode('utf-8')), 'wb' ) as output:
                bit_string = ""
                while True: #Read the data by buffer
                    data = file.read(self.buffer_size)
                    if not data:
                        break
                    for i in range(len(data)):#turn the data to bits
                        char =data[i]
                        bits = bin(char)[2:].rjust(8, '0') #[2:] to delete the bytes sign (0b) and confirm all data complete
                        bit_string += bits  
                encoded_text = self.remove_padding(bit_string) #remove padding we add in compress
                org = self.decode_text(encoded_text) #decode the data
                for i in range(0, len(org), self.buffer_size):#write the orignal data to file by buffer
                    buffer = org[i:i+self.buffer_size]
                    output.write(buffer)