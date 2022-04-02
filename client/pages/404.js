import Link from 'next/link'
import Image from 'next/image'

const NotFound = () => {
    return (
        <div className="text-center justify-center text-black text-xl mt-8 font-extrabold exo-font ">
            <h1>Oooops...</h1>
            <h2>That page cannot be found.</h2>
            <Image 
            src='/images/1_blank.png'
            width='300px'
            height='300px'>
            </Image>
            <p>Go back to the <Link href="/"><a className="hover:text-cryptid-6 underline">Homepage</a></Link></p>
           
        </div>
        
    );
}

export default NotFound;